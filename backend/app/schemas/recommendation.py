from datetime import datetime

from pydantic import BaseModel, ConfigDict


class RecommendationResponse(BaseModel):
    id: int
    incident_id: int
    resource_id: int
    score: float
    distance_km: float | None = None
    reason: str | None = None
    status: str
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


class RecommendationStatusUpdate(BaseModel):
    status: str