from datetime import datetime

from pydantic import BaseModel


class TemperatureBase(BaseModel):
    date_time: datetime
    temperature: float


class Temperature(TemperatureBase):
    id: int

    class Config:
        from_attributes = True


class TemperatureCreate(TemperatureBase):
    city_id: int


class TemperatureUpdate(TemperatureBase):
    city_id: int
