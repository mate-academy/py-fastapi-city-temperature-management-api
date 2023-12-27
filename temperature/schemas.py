from datetime import datetime
from pydantic import BaseModel

from city.schemas import City


class TemperatureBase(BaseModel):
    city_id: int
    temperature: float


class TemperatureCreate(TemperatureBase):
    pass


class Temperature(TemperatureBase):
    id: int
    date_time: datetime
    city: City

    class Config:
        orm_mode = True
