from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from app.crud.incident import (
    create_incident,
    get_incident,
    get_incidents,
    update_incident,
)
from app.db.session import get_db
from app.schemas.incident import (
    IncidentCreate,
    IncidentResponse,
)
from app.services.alert_service import generate_incident_alerts
from app.services.incident_classifier import classify_incident
from app.services.websocket_manager import manager


router = APIRouter(
    prefix="/api/incidents",
    tags=["Incidents"]
)


@router.post("/", response_model=IncidentResponse)
async def create_incident_route(
    incident_data: IncidentCreate,
    db: Session = Depends(get_db)
):
    incident = create_incident(
        db,
        incident_data
    )

    alerts = generate_incident_alerts(
        db,
        incident
    )

    await manager.broadcast({
        "type": "INCIDENT_CREATED",
        "incident_id": incident.id,
        "message": "New incident reported"
    })

    for alert in alerts:
        await manager.broadcast({
            "type": "ALERT_CREATED",
            "alert_id": alert.id,
            "incident_id": alert.incident_id,
            "level": alert.level,
            "title": alert.title,
            "message": alert.message,
        })

    return incident


@router.get(
    "/",
    response_model=list[IncidentResponse]
)
def get_all_incidents(
    db: Session = Depends(get_db)
):
    return get_incidents(db)


@router.get(
    "/{incident_id}",
    response_model=IncidentResponse
)
def get_single_incident(
    incident_id: int,
    db: Session = Depends(get_db)
):
    incident = get_incident(
        db,
        incident_id
    )

    if not incident:
        raise HTTPException(
            status_code=404,
            detail="Incident not found"
        )

    return incident


@router.post(
    "/{incident_id}/classify",
    response_model=IncidentResponse
)
def classify_existing_incident(
    incident_id: int,
    db: Session = Depends(get_db)
):
    incident = get_incident(
        db,
        incident_id
    )

    if not incident:
        raise HTTPException(
            status_code=404,
            detail="Incident not found"
        )

    classification = classify_incident(
        title=incident.title,
        description=incident.description or "",
        incident_type=incident.incident_type,
    )

    incident.incident_type = classification["incident_type"]
    incident.severity = classification["severity"]
    incident.priority = classification["priority"]

    incident.classification_confidence = (
        classification["confidence"]
    )

    incident.classification_reasoning = (
        classification["reasoning"]
    )

    db.commit()
    db.refresh(incident)

    return incident


@router.put(
    "/{incident_id}",
    response_model=IncidentResponse
)
def update_single_incident(
    incident_id: int,
    incident_data: IncidentCreate,
    db: Session = Depends(get_db)
):
    incident = update_incident(
        db,
        incident_id,
        incident_data
    )

    if not incident:
        raise HTTPException(
            status_code=404,
            detail="Incident not found"
        )

    return incident