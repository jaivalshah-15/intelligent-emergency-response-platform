from app.crud.alert import create_alert


def generate_incident_alerts(db, incident):
    alerts = []

    if incident.severity == "CRITICAL":
        alerts.append(
            create_alert(
                db=db,
                incident_id=incident.id,
                alert_type="CRITICAL_INCIDENT",
                level="CRITICAL",
                title="Critical Incident Detected",
               message=f"Critical incident reported: {incident.title}",
            )
        )

    if incident.severity == "HIGH":
        alerts.append(
            create_alert(
                db=db,
                incident_id=incident.id,
                alert_type="HIGH_SEVERITY",
                level="HIGH",
                title="High Severity Incident",
                message=f"High severity incident reported: {incident.title}",
            )
        )

    if incident.priority == "HIGH":
        alerts.append(
            create_alert(
                db=db,
                incident_id=incident.id,
                alert_type="HIGH_PRIORITY",
                level="HIGH",
                title="High Priority Incident",
                message=f"High priority incident requires attention: {incident.title}",
            )
        )

    return alerts