from datetime import datetime

from pydantic import BaseModel


class STemperatureBase(BaseModel):
    city_id: int
    date_time: datetime
    temperature: float


class STemperature(STemperatureBase):
    id: int

    class Config:
        from_attributes = True


class STemperatureCreate(STemperatureBase):
    pass


class STemperatureUpdateResult(BaseModel):
    city_id: int
    city_name: str
    success: bool
    temperature: float | None = None
    error: str | None = None
