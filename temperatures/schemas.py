from datetime import datetime

from pydantic import BaseModel

from cities.schemas import City


class TemperatureBase(BaseModel):
    date_time: datetime
    temperature: float


class TemperatureCreate(TemperatureBase):
    city_id: int


class Temperature(TemperatureBase):
    id: int
    city: City

    class Config:
        orm_mode = True
