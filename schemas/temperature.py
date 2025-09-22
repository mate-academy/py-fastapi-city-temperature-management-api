from pydantic import BaseModel
from datetime import datetime


class TemperatureBase(BaseModel):
    temperature: float
    city_id: int


class TemperatureCreate(TemperatureBase):
    pass


class Temperature(TemperatureBase):
    id: int
    date_time: datetime

    class Config:
        orm_mode = True
