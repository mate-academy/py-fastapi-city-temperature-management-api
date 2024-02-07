from pydantic import BaseModel
from datetime import datetime


class TemperatureBase(BaseModel):
    temperature: float
    date_time: datetime


class TemperatureCreate(TemperatureBase):
    city_id: int


class Temperature(TemperatureBase):
    id: int
    city_id: int

    class Config:
        orm_mode = True
