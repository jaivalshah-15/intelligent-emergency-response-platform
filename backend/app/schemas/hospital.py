from datetime import datetime

from pydantic import BaseModel, ConfigDict


class HospitalCreate(BaseModel):
    name: str
    address: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    total_beds: int = 0
    available_beds: int = 0
    emergency_capacity: int = 0
    status: str = "AVAILABLE"


class HospitalUpdate(BaseModel):
    name: str | None = None
    address: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    total_beds: int | None = None
    available_beds: int | None = None
    emergency_capacity: int | None = None
    status: str | None = None


class HospitalResponse(BaseModel):
    id: int
    name: str
    address: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    total_beds: int
    available_beds: int
    emergency_capacity: int
    status: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)