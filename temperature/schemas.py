from datetime import datetime

from pydantic import BaseModel

from city.models import DBCity


class TemperatureBase(BaseModel):
    city_id: int
    temperature: float
    date_time: datetime


class TemperatureCreate(TemperatureBase):
    pass


class Temperature(TemperatureBase):
    id: int
    city_id: int

    class Config:
        from_attributes = True
