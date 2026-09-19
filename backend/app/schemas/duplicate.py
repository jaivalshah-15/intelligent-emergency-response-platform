from datetime import datetime

from pydantic import BaseModel, ConfigDict


class DuplicateCandidateResponse(BaseModel):
    id: int
    incident_id: int
    possible_duplicate_id: int
    similarity_score: float
    matching_factors: str | None = None
    status: str
    created_at: datetime

    model_config = ConfigDict(
        from_attributes=True
    )


class DuplicateStatusUpdate(BaseModel):
    status: str