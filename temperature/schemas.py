from pydantic import BaseModel
from datetime import datetime


class TemperatureBase(BaseModel):
    city_id: int
    date_time: datetime
    temperature: float


class Temperature(TemperatureBase):
    id: int

    class Config:
        orm_mode = True


class TemperatureCreate(TemperatureBase):
    city_id: int
    date_time: datetime
    temperature: float


class TemperatureUpdate(BaseModel):
    city_id: int
    date_time: datetime
    temperature: float
