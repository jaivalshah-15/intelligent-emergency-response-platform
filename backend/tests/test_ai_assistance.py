from types import SimpleNamespace

from app.services.ai_assistant import build_incident_summary


def test_incident_summary():
    incident = SimpleNamespace(
        id=15,
        title="Factory Fire",
        description="Large fire with several people trapped.",
        incident_type="FIRE",
        severity="CRITICAL",
        priority="HIGH",
        classification_confidence=0.95,
        classification_reasoning=(
            "Critical emergency indicators were detected."
        ),
        address="Vadodara Industrial Area",
        latitude=22.3072,
        longitude=73.1812,
    )

    result = build_incident_summary(incident)

    assert result["incident_id"] == 15
    assert "factory fire" in result["summary"].lower()
    assert result["situation"]
    assert len(result["key_findings"]) >= 3
    assert len(result["recommended_actions"]) >= 3
    assert "FIRE_TRUCK" in result["resource_needs"]
    assert result["generated_by"] == "local-ai-assistant"


def test_medical_resource_needs():
    incident = SimpleNamespace(
        id=20,
        title="Medical Emergency",
        description="Patient needs urgent medical assistance.",
        incident_type="MEDICAL",
        severity="HIGH",
        priority="HIGH",
        classification_confidence=0.85,
        classification_reasoning="Medical indicators were detected.",
        address="Demo Location",
        latitude=None,
        longitude=None,
    )

    result = build_incident_summary(incident)

    assert "AMBULANCE" in result["resource_needs"]
    assert "MEDICAL_TEAM" in result["resource_needs"]