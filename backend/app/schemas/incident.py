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
    description: str
    incident_type: str
    severity: str
    priority: str
    status: str
    source: str
    address: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)