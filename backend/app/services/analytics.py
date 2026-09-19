from sqlalchemy import func
from sqlalchemy.orm import Session

from app.models.alert import Alert
from app.models.assignment import ResourceAssignment
from app.models.incident import Incident
from app.models.resource import Resource


def get_analytics(db: Session) -> dict:
    total_incidents = db.query(Incident).count()

    active_incidents = (
        db.query(Incident)
        .filter(Incident.status == "ACTIVE")
        .count()
    )

    critical_incidents = (
        db.query(Incident)
        .filter(Incident.severity == "CRITICAL")
        .count()
    )

    high_priority_incidents = (
        db.query(Incident)
        .filter(Incident.priority == "HIGH")
        .count()
    )

    total_alerts = db.query(Alert).count()

    active_alerts = (
        db.query(Alert)
        .filter(Alert.status == "ACTIVE")
        .count()
    )

    resolved_alerts = (
        db.query(Alert)
        .filter(Alert.status == "RESOLVED")
        .count()
    )

    total_resources = db.query(Resource).count()

    available_resources = (
        db.query(Resource)
        .filter(Resource.status == "AVAILABLE")
        .count()
    )

    assigned_resources = (
        db.query(Resource)
        .filter(Resource.status == "ASSIGNED")
        .count()
    )

    total_assignments = db.query(ResourceAssignment).count()

    active_assignments = (
        db.query(ResourceAssignment)
        .filter(ResourceAssignment.status == "ASSIGNED")
        .count()
    )

    incidents_by_type = {
        str(row[0]): row[1]
        for row in (
            db.query(
                Incident.incident_type,
                func.count(Incident.id)
            )
            .group_by(Incident.incident_type)
            .all()
        )
    }

    incidents_by_severity = {
        str(row[0]): row[1]
        for row in (
            db.query(
                Incident.severity,
                func.count(Incident.id)
            )
            .group_by(Incident.severity)
            .all()
        )
    }

    incidents_by_priority = {
        str(row[0]): row[1]
        for row in (
            db.query(
                Incident.priority,
                func.count(Incident.id)
            )
            .group_by(Incident.priority)
            .all()
        )
    }

    alerts_by_level = {
        str(row[0]): row[1]
        for row in (
            db.query(
                Alert.level,
                func.count(Alert.id)
            )
            .group_by(Alert.level)
            .all()
        )
    }

    return {
        "total_incidents": total_incidents,
        "active_incidents": active_incidents,
        "critical_incidents": critical_incidents,
        "high_priority_incidents": high_priority_incidents,
        "total_alerts": total_alerts,
        "active_alerts": active_alerts,
        "resolved_alerts": resolved_alerts,
        "total_resources": total_resources,
        "available_resources": available_resources,
        "assigned_resources": assigned_resources,
        "total_assignments": total_assignments,
        "active_assignments": active_assignments,
        "incidents_by_type": incidents_by_type,
        "incidents_by_severity": incidents_by_severity,
        "incidents_by_priority": incidents_by_priority,
        "alerts_by_level": alerts_by_level,
    }