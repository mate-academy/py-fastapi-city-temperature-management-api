from datetime import datetime

from pydantic import BaseModel

from city.schemas import City


class TemperatureBase(BaseModel):
    temperature: float


class TemperatureCreate(TemperatureBase):
    city_id: int


class Temperature(TemperatureBase):
    id: int
    city: City
    date_time: datetime

    class Config:
        from_attributes = True
