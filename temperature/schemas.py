from pydantic import BaseModel
from datetime import datetime


class TemperatureBase(BaseModel):
    city_id: int
    temperature: float
    date_time: datetime


class TemperatureCreate(TemperatureBase):
    pass


class Temperature(TemperatureBase):
    id: int

    class Config:
        orm_mode = True
