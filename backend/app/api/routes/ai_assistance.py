from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.db.session import get_db
from app.models.incident import Incident
from app.schemas.ai_assistance import IncidentSummaryResponse
from app.services.ai_assistant import build_incident_summary


router = APIRouter(
    prefix="/api/incidents",
    tags=["AI Assistance"]
)


@router.get(
    "/{incident_id}/summary",
    response_model=IncidentSummaryResponse
)
def get_incident_summary(
    incident_id: int,
    db: Session = Depends(get_db)
):
    incident = (
        db.query(Incident)
        .filter(Incident.id == incident_id)
        .first()
    )

    if not incident:
        raise HTTPException(
            status_code=404,
            detail="Incident not found"
        )

    return build_incident_summary(incident)