from datetime import datetime

from pydantic import BaseModel


class TemperatureBase(BaseModel):
    temperature: float
    date_time: datetime


class TemperatureCreate(BaseModel):
    temperature: float
    city_id: int


class Temperature(TemperatureBase):
    id: int
    city_id: int
    class Config:
        orm_mode = True
