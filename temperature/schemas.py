import datetime

from pydantic import BaseModel


class TemperatureBase(BaseModel):
    city_id: int
    temperature: float
    date_time: datetime.datetime


class TemperatureCreate(TemperatureBase):
    pass


class Temperature(TemperatureBase):
    id: int

    class Config:
        from_attributes = True
