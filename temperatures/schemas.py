from datetime import datetime

from pydantic import BaseModel, ConfigDict


class TemperatureBase(BaseModel):
    city_id: int
    date_time: datetime
    temperature: float


class Temperature(TemperatureBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class TemperatureCreate(TemperatureBase):
    pass


class TemperatureUpdateResult(BaseModel):
    city_id: int
    city_name: str
    success: bool
    temperature: float | None = None
    error: str | None = None