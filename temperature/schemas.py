from datetime import datetime

from pydantic import BaseModel


class TemperatureBase(BaseModel):
    city_id: int
    temperature: float
    date_time: datetime


class Temperature(TemperatureBase):
    id: int

    class Config:
        orm_mode = True
