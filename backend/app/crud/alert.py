from datetime import datetime, timezone

from sqlalchemy.orm import Session

from app.models.alert import Alert


def create_alert(
    db: Session,
    incident_id: int | None,
    alert_type: str,
    level: str,
    title: str,
    message: str,
):
    alert = Alert(
        incident_id=incident_id,
        alert_type=alert_type,
        level=level,
        title=title,
        message=message,
        status="ACTIVE",
    )

    db.add(alert)
    db.commit()
    db.refresh(alert)

    return alert


def get_alerts(
    db: Session,
    status: str | None = None,
):
    query = db.query(Alert)

    if status is not None:
        query = query.filter(Alert.status == status)

    return query.order_by(Alert.created_at.desc()).all()


def get_alert(
    db: Session,
    alert_id: int,
):
    return db.query(Alert).filter(Alert.id == alert_id).first()


def acknowledge_alert(
    db: Session,
    alert_id: int,
):
    alert = get_alert(db, alert_id)

    if not alert:
        return None

    alert.status = "ACKNOWLEDGED"
    alert.acknowledged_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(alert)

    return alert


def resolve_alert(
    db: Session,
    alert_id: int,
):
    alert = get_alert(db, alert_id)

    if not alert:
        return None

    alert.status = "RESOLVED"
    alert.resolved_at = datetime.now(timezone.utc)

    db.commit()
    db.refresh(alert)

    return alert