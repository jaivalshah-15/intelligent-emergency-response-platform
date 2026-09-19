from datetime import datetime
from pydantic import BaseModel, ConfigDict


class IncidentCreate(BaseModel):
    title: str
    description: str
    incident_type: str
    source: str
    address: str | None = None
    latitude: float | None = None
    longitude: float | None = None


class IncidentResponse(BaseModel):
    id: int
    title: str
    description: str | None = None
    incident_type: str
    severity: str
    priority: str

    classification_confidence: float | None = None
    classification_reasoning: str | None = None

    status: str
    source: str
    address: str | None = None
    latitude: float | None = None
    longitude: float | None = None

    reported_at: datetime
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)

class IncidentClassificationResult(BaseModel):
    incident_type: str
    severity: str
    priority: str
    confidence: float
    reasoning: str