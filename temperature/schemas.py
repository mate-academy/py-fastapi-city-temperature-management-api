from pydantic import BaseModel
from datetime import datetime

from city.schemas import City


class TemperatureBase(BaseModel):
    date_time: datetime
    temperature: str


class TemperatureCreate(TemperatureBase):
    city_id: int


class Temperature(TemperatureBase):
    id: int
    city: City

    class Config:
        from_attributes = True
