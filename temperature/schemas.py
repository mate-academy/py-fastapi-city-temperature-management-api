from pydantic import BaseModel
from datetime import datetime
from city.schemas import CityBase


class TemperatureBase(BaseModel):
    city_id: int
    date_time: datetime
    temperature: float


class TemperatureCreate(BaseModel):
    city_id: int
    date_time: datetime
    temperature: float


class TemperatureRead(BaseModel):
    id: int
    city_id: int
    city: CityBase
    date_time: datetime
    temperature: float
