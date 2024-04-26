from pydantic import BaseModel
from datetime import datetime

from city.schemas import City


class TemperatureBase(BaseModel):
    date_time: datetime
    temperature: float


class TemperatureCreate(TemperatureBase):
    pass


class Temperature(TemperatureBase):
    id: int
    city_id: int
    city: City

    class Config:
        orm_mode = True
