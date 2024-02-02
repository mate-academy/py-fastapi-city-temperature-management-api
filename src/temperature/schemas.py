from datetime import datetime
from pydantic import BaseModel

from src.city.schemas import City


class TemperatureBase(BaseModel):
    temperature: int
    date_time: datetime


class TemperatureCreate(TemperatureBase):
    city_id: int


class Temperature(TemperatureBase):
    id: int
    city: City
