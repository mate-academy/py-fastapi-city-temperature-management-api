from typing import Optional

from pydantic import BaseModel
from datetime import datetime


class TemperatureBase(BaseModel):
    city_id: int
    date_time: datetime
    temperature: float


class TemperatureCreate(TemperatureBase):
    pass


class TemperatureUpdate(TemperatureBase):
    date_time: Optional[datetime] = None
    temperature: Optional[float] = None


class Temperature(TemperatureBase):
    id: int

    class Config:
        orm_mode = True
