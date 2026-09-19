from datetime import datetime

from pydantic import BaseModel, ConfigDict


class ResourceCreate(BaseModel):
    name: str
    resource_type: str
    status: str = "AVAILABLE"
    latitude: float | None = None
    longitude: float | None = None


class ResourceUpdate(BaseModel):
    name: str | None = None
    resource_type: str | None = None
    status: str | None = None
    latitude: float | None = None
    longitude: float | None = None


class ResourceResponse(BaseModel):
    id: int
    name: str
    resource_type: str
    status: str
    latitude: float | None = None
    longitude: float | None = None
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)