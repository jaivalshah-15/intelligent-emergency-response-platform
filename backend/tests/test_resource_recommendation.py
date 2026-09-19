from types import SimpleNamespace

from app.services.resource_recommender import (
    calculate_distance_km,
    calculate_resource_score,
)


def test_fire_resource_match():
    incident = SimpleNamespace(
        incident_type="FIRE",
        severity="CRITICAL",
        priority="HIGH",
        latitude=23.0225,
        longitude=72.5714,
    )

    resource = SimpleNamespace(
        resource_type="FIRE_TRUCK",
        status="AVAILABLE",
        latitude=23.0230,
        longitude=72.5718,
    )

    result = calculate_resource_score(
        incident,
        resource
    )

    assert result["score"] > 0
    assert result["distance_km"] is not None


def test_distance():
    distance = calculate_distance_km(
        23.0225,
        72.5714,
        23.0230,
        72.5718,
    )

    assert distance >= 0