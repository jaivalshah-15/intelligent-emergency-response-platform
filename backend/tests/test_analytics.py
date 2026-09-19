from app.db.session import SessionLocal
from app.services.analytics import get_analytics


def test_analytics_structure():
    db = SessionLocal()

    try:
        result = get_analytics(db)

        assert "total_incidents" in result
        assert "active_incidents" in result
        assert "critical_incidents" in result
        assert "high_priority_incidents" in result

        assert "total_alerts" in result
        assert "active_alerts" in result
        assert "resolved_alerts" in result

        assert "total_resources" in result
        assert "available_resources" in result
        assert "assigned_resources" in result

        assert "total_assignments" in result
        assert "active_assignments" in result

        assert isinstance(result["incidents_by_type"], dict)
        assert isinstance(result["incidents_by_severity"], dict)
        assert isinstance(result["incidents_by_priority"], dict)
        assert isinstance(result["alerts_by_level"], dict)

    finally:
        db.close()