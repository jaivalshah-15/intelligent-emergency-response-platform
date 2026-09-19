from app.models.incident import Incident


def build_incident_summary(incident: Incident) -> dict:
    incident_type = (incident.incident_type or "OTHER").upper()
    severity = (incident.severity or "MEDIUM").upper()
    priority = (incident.priority or "NORMAL").upper()

    title = incident.title or "Emergency incident"
    description = incident.description or "No description provided."

    resource_map = {
        "FIRE": [
            "FIRE_TRUCK",
            "RESCUE_TEAM",
            "AMBULANCE",
        ],
        "FLOOD": [
            "RESCUE_TEAM",
            "AMBULANCE",
            "FLOOD_RESCUE_EQUIPMENT",
        ],
        "ACCIDENT": [
            "AMBULANCE",
            "RESCUE_TEAM",
        ],
        "INDUSTRIAL": [
            "FIRE_TRUCK",
            "RESCUE_TEAM",
            "AMBULANCE",
            "SAFETY_EQUIPMENT",
        ],
        "MEDICAL": [
            "AMBULANCE",
            "MEDICAL_TEAM",
        ],
        "OTHER": [
            "COORDINATOR_ASSESSMENT",
        ],
    }

    severity_text = {
        "CRITICAL": "Immediate coordinator attention is required.",
        "HIGH": "Urgent response and close monitoring are recommended.",
        "MEDIUM": "Routine response coordination is recommended.",
        "LOW": "Monitor the incident and reassess if conditions change.",
    }

    key_findings = [
        f"Incident type: {incident_type}",
        f"Severity: {severity}",
        f"Priority: {priority}",
    ]

    if incident.classification_confidence is not None:
        key_findings.append(
            f"Classification confidence: "
            f"{round(incident.classification_confidence * 100)}%"
        )

    if incident.classification_reasoning:
        key_findings.append(
            f"AI classification reasoning: "
            f"{incident.classification_reasoning}"
        )

    recommended_actions = [
        severity_text.get(
            severity,
            "Review the incident and determine the appropriate response."
        ),
        "Coordinator should review the incident details before dispatching resources.",
        "Verify the incident location and current situation with available information.",
    ]

    if severity in ["CRITICAL", "HIGH"]:
        recommended_actions.append(
            "Prioritize the recommended emergency resources for coordinator review."
        )

    summary = (
        f"{title} is classified as a {severity.lower()} {incident_type.lower()} "
        f"incident with {priority.lower()} priority. "
        f"{description}"
    )

    if incident.address:
        situation = (
            f"Reported location: {incident.address}. "
            f"{severity_text.get(severity, '')}"
        )
    else:
        situation = severity_text.get(
            severity,
            "Review the incident details."
        )

    if incident.latitude is not None and incident.longitude is not None:
        situation += (
            f" Coordinates: {incident.latitude}, {incident.longitude}."
        )

    return {
        "incident_id": incident.id,
        "summary": summary,
        "situation": situation,
        "key_findings": key_findings,
        "recommended_actions": recommended_actions,
        "resource_needs": resource_map.get(
            incident_type,
            resource_map["OTHER"]
        ),
        "generated_by": "local-ai-assistant",
    }