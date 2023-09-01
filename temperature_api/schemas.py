from datetime import datetime

from pydantic import BaseModel
from typing import Optional


class TemperatureBase(BaseModel):
    city_id: int
    date_time: datetime
    temperature: float


class TemperatureCreate(TemperatureBase):
    pass


class TemperatureUpdate(TemperatureBase):
    pass


class Temperature(TemperatureBase):
    id: int

    class Config:
        from_attributes = True
