from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session

from app.crud.alert import (
    acknowledge_alert,
    get_alert,
    get_alerts,
    resolve_alert,
)
from app.db.session import get_db
from app.schemas.alert import AlertResponse
from app.services.websocket_manager import manager

router = APIRouter(
    prefix="/api/alerts",
    tags=["Alerts"]
)


@router.get("/", response_model=list[AlertResponse])
def get_all_alerts(
    status: str | None = None,
    db: Session = Depends(get_db),
):
    return get_alerts(
        db,
        status=status
    )


@router.get("/{alert_id}", response_model=AlertResponse)
def get_single_alert(
    alert_id: int,
    db: Session = Depends(get_db),
):
    alert = get_alert(db, alert_id)

    if not alert:
        raise HTTPException(
            status_code=404,
            detail="Alert not found"
        )

    return alert


@router.patch("/{alert_id}/acknowledge", response_model=AlertResponse)
async def acknowledge(
    alert_id: int,
    db: Session = Depends(get_db),
):
    alert = acknowledge_alert(db, alert_id)

    if not alert:
        raise HTTPException(
            status_code=404,
            detail="Alert not found"
        )

    await manager.broadcast({
        "type": "ALERT_UPDATED",
        "alert_id": alert.id,
        "incident_id": alert.incident_id,
        "status": alert.status,
    })

    return alert


@router.patch("/{alert_id}/resolve", response_model=AlertResponse)
async def resolve(
    alert_id: int,
    db: Session = Depends(get_db),
):
    alert = resolve_alert(db, alert_id)

    if not alert:
        raise HTTPException(
            status_code=404,
            detail="Alert not found"
        )

    await manager.broadcast({
        "type": "ALERT_UPDATED",
        "alert_id": alert.id,
        "incident_id": alert.incident_id,
        "status": alert.status,
    })

    return alert