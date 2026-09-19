from math import atan2, cos, radians, sin, sqrt


RESOURCE_RULES = {
    "FIRE": [
        "FIRE_TRUCK",
        "RESCUE_TEAM",
        "AMBULANCE",
    ],
    "FLOOD": [
        "RESCUE_TEAM",
        "AMBULANCE",
        "EQUIPMENT",
    ],
    "ACCIDENT": [
        "AMBULANCE",
        "RESCUE_TEAM",
    ],
    "INDUSTRIAL": [
        "FIRE_TRUCK",
        "RESCUE_TEAM",
        "AMBULANCE",
        "EQUIPMENT",
    ],
    "MEDICAL": [
        "AMBULANCE",
        "MEDICAL_TEAM",
    ],
}


def calculate_distance_km(
    lat1,
    lon1,
    lat2,
    lon2
):
    earth_radius = 6371.0

    lat1 = radians(lat1)
    lon1 = radians(lon1)
    lat2 = radians(lat2)
    lon2 = radians(lon2)

    dlat = lat2 - lat1
    dlon = lon2 - lon1

    a = (
        sin(dlat / 2) ** 2
        + cos(lat1)
        * cos(lat2)
        * sin(dlon / 2) ** 2
    )

    c = 2 * atan2(
        sqrt(a),
        sqrt(1 - a)
    )

    return earth_radius * c


def calculate_resource_score(
    incident,
    resource
):
    score = 0.0
    reasons = []

    required_types = RESOURCE_RULES.get(
        incident.incident_type,
        []
    )

    if resource.resource_type in required_types:
        score += 40
        reasons.append("Type match")

    if incident.severity == "CRITICAL":
        score += 25
        reasons.append("Critical severity")
    elif incident.severity == "HIGH":
        score += 15
        reasons.append("High severity")

    if incident.priority == "HIGH":
        score += 15
        reasons.append("High priority")
    elif incident.priority == "MEDIUM":
        score += 8
        reasons.append("Medium priority")

    distance = None

    if (
        incident.latitude is not None
        and incident.longitude is not None
        and resource.latitude is not None
        and resource.longitude is not None
    ):
        distance = calculate_distance_km(
            incident.latitude,
            incident.longitude,
            resource.latitude,
            resource.longitude,
        )

        if distance <= 2:
            score += 20
            reasons.append("Very close")
        elif distance <= 5:
            score += 15
            reasons.append("Nearby")
        elif distance <= 10:
            score += 8
            reasons.append("Moderate distance")

    return {
        "score": round(score, 2),
        "distance_km": (
            round(distance, 2)
            if distance is not None
            else None
        ),
        "reason": ", ".join(reasons),
    }


def recommend_resources(
    incident,
    resources
):
    recommendations = []

    for resource in resources:
        if resource.status != "AVAILABLE":
            continue

        result = calculate_resource_score(
            incident,
            resource
        )

        if result["score"] <= 0:
            continue

        recommendations.append({
            "resource": resource,
            "score": result["score"],
            "distance_km": result["distance_km"],
            "reason": result["reason"],
        })

    recommendations.sort(
        key=lambda x: x["score"],
        reverse=True
    )

    return recommendations