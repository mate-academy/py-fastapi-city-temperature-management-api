import datetime

from pydantic import BaseModel


class TemperatureBase(BaseModel):
    date_time: datetime.datetime
    temperature: int
    city_id: int


class TemperatureCreate(BaseModel):
    temperature: float
    city_id: int


class Temperature(BaseModel):
    id: int
    date_time: datetime.datetime
    temperature: int
    city_id: int
