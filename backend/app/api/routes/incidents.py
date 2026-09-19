from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud.incident import (
    create_incident,
    get_incident,
    get_incidents,
    update_incident,
)

from app.schemas.incident import (
    IncidentCreate,
    IncidentResponse,
)

from app.db.session import get_db


router = APIRouter(
    prefix="/api/incidents",
    tags=["Incidents"]
)


@router.post("/", response_model=IncidentResponse)
def create_incident_route(
    incident_data: IncidentCreate,
    db: Session = Depends(get_db)
):
    return create_incident(db, incident_data)


@router.get("/", response_model=list[IncidentResponse])
def get_all_incidents(
    db: Session = Depends(get_db)
):
    return get_incidents(db)


@router.get("/{incident_id}", response_model=IncidentResponse)
def get_single_incident(
    incident_id: int,
    db: Session = Depends(get_db)
):
    incident = get_incident(db, incident_id)

    if not incident:
        raise HTTPException(
            status_code=404,
            detail="Incident not found"
        )

    return incident


@router.put("/{incident_id}", response_model=IncidentResponse)
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