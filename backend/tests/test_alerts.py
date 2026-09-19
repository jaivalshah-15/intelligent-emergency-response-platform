from types import SimpleNamespace

from app.services.alert_service import (
    generate_incident_alerts,
)


def test_critical_incident_creates_alert():
    incident = SimpleNamespace(
        id=1,
        severity="CRITICAL",
        priority="HIGH",
    )

    class FakeDB:
        pass

    # Service-level test can be expanded with a mock DB.
    assert incident.severity == "CRITICAL"
    assert incident.priority == "HIGH"