from pydantic import BaseModel


class IncidentSummaryResponse(BaseModel):
    incident_id: int
    summary: str
    situation: str
    key_findings: list[str]
    recommended_actions: list[str]
    resource_needs: list[str]
    generated_by: str