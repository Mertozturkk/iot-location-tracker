from typing import Optional

from pydantic import BaseModel
import datetime


class DeviceCreate(BaseModel):
    name: str
    serial_number: str
    model: str
    is_active: Optional[bool] = True


class DeviceResponse(BaseModel):
    id: int
    name: str
    serial_number: str
    model: str
    is_active: bool

    class Config:
        from_attributes = True


class LocationCreate(BaseModel):
    device_id: int
    latitude: float
    longitude: float
    altitude: Optional[float] = None
    speed: Optional[float] = None
    direction: Optional[float] = None
    timestamp: datetime.datetime


class LocationResponse(BaseModel):
    device_id: int
    latitude: float
    longitude: float
    altitude: Optional[float] = None
    speed: Optional[float] = None
    direction: Optional[float] = None

    class Config:
        from_attributes = True
