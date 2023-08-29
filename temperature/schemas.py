from datetime import datetime

from pydantic import BaseModel

from city.schemas import City


class TemperatureBase(BaseModel):
    temperature: float


class TemperatureCreate(TemperatureBase):
    city_id: int


class Temperature(TemperatureBase):
    id: int
    date_time: datetime
    city_id: int

    class Config:
        orm_mode = True
