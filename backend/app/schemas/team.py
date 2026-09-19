from datetime import datetime

from pydantic import BaseModel, ConfigDict


class TeamCreate(BaseModel):
    name: str
    team_type: str
    status: str = "AVAILABLE"
    latitude: float | None = None
    longitude: float | None = None


class TeamUpdate(BaseModel):
    name: str | None = None
    team_type: str | None = None
    status: str | None = None
    latitude: float | None = None
    longitude: float | None = None


class TeamResponse(BaseModel):
    id: int
    name: str
    team_type: str
    status: str
    latitude: float | None = None
    longitude: float | None = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)