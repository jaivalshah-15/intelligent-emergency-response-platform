from app.services.incident_classifier import classify_incident


def test_critical_fire():
    result = classify_incident(
        "Factory Fire",
        "Large fire. Several people may be trapped.",
        "FIRE"
    )

    assert result["incident_type"] == "FIRE"
    assert result["severity"] == "CRITICAL"
    assert result["priority"] == "HIGH"
    assert result["confidence"] >= 0.9