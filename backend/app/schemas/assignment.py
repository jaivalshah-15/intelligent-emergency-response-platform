from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AssignmentCreate(BaseModel):
    incident_id: int
    resource_id: int


class AssignmentResponse(BaseModel):
    id: int
    incident_id: int
    resource_id: int
    status: str
    assigned_at: datetime
    released_at: datetime | None = None

    model_config = ConfigDict(
        from_attributes=True
    )