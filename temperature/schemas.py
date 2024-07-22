from datetime import datetime
from pydantic import BaseModel
from city.schemas import City


class TemperatureBase(BaseModel):
    temperature: float
    date_time: datetime


class TemperatureCreate(TemperatureBase):
    city_id: int


class Temperature(TemperatureBase):
    id: int
    city: City

    class Config:
        from_attributes = True
