from datetime import datetime
from difflib import SequenceMatcher
from math import atan2, cos, radians, sin, sqrt

from app.models.incident import Incident


def text_similarity(text_a: str, text_b: str) -> float:
    text_a = " ".join(text_a.lower().split())
    text_b = " ".join(text_b.lower().split())

    if not text_a or not text_b:
        return 0.0

    return SequenceMatcher(
        None,
        text_a,
        text_b
    ).ratio()


def calculate_distance_km(
    lat1: float,
    lon1: float,
    lat2: float,
    lon2: float
) -> float:
    earth_radius_km = 6371.0

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

    return earth_radius_km * c


def location_similarity(
    incident_a,
    incident_b
) -> float:
    if (
        incident_a.latitude is None
        or incident_a.longitude is None
        or incident_b.latitude is None
        or incident_b.longitude is None
    ):
        return 0.0

    distance = calculate_distance_km(
        incident_a.latitude,
        incident_a.longitude,
        incident_b.latitude,
        incident_b.longitude
    )

    if distance <= 1:
        return 1.0

    if distance <= 3:
        return 0.7

    if distance <= 5:
        return 0.4

    return 0.0


def time_similarity(
    incident_a,
    incident_b
) -> float:
    time_a: datetime = incident_a.reported_at
    time_b: datetime = incident_b.reported_at

    difference_minutes = abs(
        (time_a - time_b).total_seconds()
    ) / 60

    if difference_minutes <= 10:
        return 1.0

    if difference_minutes <= 30:
        return 0.7

    if difference_minutes <= 60:
        return 0.4

    return 0.0


def detect_duplicate_score(
    incident_a,
    incident_b
):
    text_a = (
        f"{incident_a.title} "
        f"{incident_a.description or ''}"
    )

    text_b = (
        f"{incident_b.title} "
        f"{incident_b.description or ''}"
    )

    text_score = text_similarity(
        text_a,
        text_b
    )

    type_score = (
        1.0
        if incident_a.incident_type
        == incident_b.incident_type
        else 0.0
    )

    location_score = location_similarity(
        incident_a,
        incident_b
    )

    time_score = time_similarity(
        incident_a,
        incident_b
    )

    final_score = (
        text_score * 0.45
        + type_score * 0.20
        + location_score * 0.20
        + time_score * 0.15
    )

    matching_factors = []

    if text_score >= 0.65:
        matching_factors.append("Similar text")

    if type_score == 1.0:
        matching_factors.append("Same incident type")

    if location_score >= 0.7:
        matching_factors.append("Nearby location")

    if time_score >= 0.7:
        matching_factors.append("Close reporting time")

    return {
        "score": round(final_score, 2),
        "matching_factors": matching_factors,
    }


def find_possible_duplicates(
    db,
    new_incident
):
    existing_incidents = (
        db.query(Incident)
        .filter(
            Incident.id != new_incident.id
        )
        .order_by(
            Incident.reported_at.desc()
        )
        .limit(100)
        .all()
    )

    possible_duplicates = []

    for incident in existing_incidents:
        result = detect_duplicate_score(
            new_incident,
            incident
        )

        if result["score"] >= 0.65:
            possible_duplicates.append(
                {
                    "incident": incident,
                    "score": result["score"],
                    "matching_factors": result[
                        "matching_factors"
                    ],
                }
            )

    return possible_duplicates