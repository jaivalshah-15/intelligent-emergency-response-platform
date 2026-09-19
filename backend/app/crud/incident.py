from sqlalchemy.orm import Session

from app.models.incident import Incident
from app.schemas.incident import IncidentCreate


def create_incident(db: Session, incident_data: IncidentCreate):
    incident = Incident(
        title=incident_data.title,
        description=incident_data.description,
        incident_type=incident_data.incident_type,
        source=incident_data.source,
        address=incident_data.address,
        latitude=incident_data.latitude,
        longitude=incident_data.longitude,
        severity="MEDIUM",
        priority="NORMAL",
        status="ACTIVE",
    )

    db.add(incident)
    db.commit()
    db.refresh(incident)

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