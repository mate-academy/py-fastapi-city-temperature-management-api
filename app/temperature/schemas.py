import datetime

from pydantic import BaseModel

from app.city.schemas import City


class TemperatureBase(BaseModel):
    temperature: float
    date_time: datetime.datetime


class TemperatureCreate(TemperatureBase):
    pass


class Temperature(TemperatureBase):
    id: int
    city: City

    class Config:
        from_attributes = True
