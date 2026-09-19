from pydantic import BaseModel


class AnalyticsResponse(BaseModel):
    total_incidents: int
    active_incidents: int
    critical_incidents: int
    high_priority_incidents: int

    total_alerts: int
    active_alerts: int
    resolved_alerts: int

    total_resources: int
    available_resources: int
    assigned_resources: int

    total_assignments: int
    active_assignments: int

    incidents_by_type: dict[str, int]
    incidents_by_severity: dict[str, int]
    incidents_by_priority: dict[str, int]
    alerts_by_level: dict[str, int]