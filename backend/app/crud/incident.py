from sqlalchemy import or_
from sqlalchemy.orm import Session
from app.crud.duplicate import create_duplicate_candidate
from app.models.alert import Alert
from app.models.assignment import ResourceAssignment
from app.models.duplicate import DuplicateCandidate
from app.models.incident import Incident
from app.models.recommendation import ResourceRecommendation
from app.models.resource import Resource
from app.schemas.incident import IncidentCreate
from app.services.duplicate_detector import find_possible_duplicates
from app.services.incident_classifier import classify_incident

def create_incident(db: Session, incident_data: IncidentCreate):
    classification = classify_incident(
        title=incident_data.title,
        description=incident_data.description or "",
        incident_type=incident_data.incident_type,
    )

    incident = Incident(
        title=incident_data.title,
        description=incident_data.description,

        incident_type=classification["incident_type"],
        severity=classification["severity"],
        priority=classification["priority"],

        classification_confidence=classification["confidence"],
        classification_reasoning=classification["reasoning"],

        status="ACTIVE",
        source=incident_data.source,
        address=incident_data.address,
        latitude=incident_data.latitude,
        longitude=incident_data.longitude,
    )

    db.add(incident)
    db.commit()
    db.refresh(incident)
    possible_duplicates = find_possible_duplicates(
    db,
    incident
    )

    for duplicate in possible_duplicates:
        create_duplicate_candidate(
            db=db,
            incident_id=incident.id,
            possible_duplicate_id=duplicate["incident"].id,
            similarity_score=duplicate["score"],
            matching_factors=", ".join(
                duplicate["matching_factors"]
            ),
        )
    return incident


def get_incident(db: Session, incident_id: int):
    return db.query(Incident).filter(Incident.id == incident_id).first()


def get_incidents(db: Session):
    return db.query(Incident).all()


def update_incident(
    db: Session,
    incident_id: int,
    incident_data: IncidentCreate
):
    incident = (
        db.query(Incident)
        .filter(Incident.id == incident_id)
        .first()
    )

    if not incident:
        return None

    incident.title = incident_data.title
    incident.description = incident_data.description
    incident.incident_type = incident_data.incident_type
    incident.source = incident_data.source
    incident.address = incident_data.address
    incident.latitude = incident_data.latitude
    incident.longitude = incident_data.longitude

    db.commit()
    db.refresh(incident)

    return incident


def resolve_and_delete_incident(
    db: Session,
    incident_id: int
):
    incident = (
        db.query(Incident)
        .filter(Incident.id == incident_id)
        .first()
    )

    if not incident:
        return None

    # Find assignments so assigned resources can be released
    assignments = (
        db.query(ResourceAssignment)
        .filter(
            ResourceAssignment.incident_id == incident_id,
            ResourceAssignment.status == "ASSIGNED"
        )
        .all()
    )

    # Release assigned resources
    for assignment in assignments:
        resource = (
            db.query(Resource)
            .filter(Resource.id == assignment.resource_id)
            .first()
        )

        if resource:
            resource.status = "AVAILABLE"

    # Delete assignments
    db.query(ResourceAssignment).filter(
        ResourceAssignment.incident_id == incident_id
    ).delete(synchronize_session=False)

    # Delete recommendations
    db.query(ResourceRecommendation).filter(
        ResourceRecommendation.incident_id == incident_id
    ).delete(synchronize_session=False)

    # Delete duplicate records involving this incident
    db.query(DuplicateCandidate).filter(
        or_(
            DuplicateCandidate.incident_id == incident_id,
            DuplicateCandidate.possible_duplicate_id == incident_id
        )
    ).delete(synchronize_session=False)

    # Delete related alerts
    db.query(Alert).filter(
        Alert.incident_id == incident_id
    ).delete(synchronize_session=False)

    # Delete the incident
    db.delete(incident)

    db.commit()

    return {
        "incident_id": incident_id,
        "status": "RESOLVED",
        "message": "Incident resolved and deleted successfully"
    }