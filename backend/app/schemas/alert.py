from datetime import datetime

from pydantic import BaseModel, ConfigDict


class AlertResponse(BaseModel):
    id: int
    incident_id: int | None = None
    alert_type: str
    level: str
    title: str
    message: str
    status: str
    created_at: datetime
    acknowledged_at: datetime | None = None
    resolved_at: datetime | None = None

    model_config = ConfigDict(
        from_attributes=True
    )