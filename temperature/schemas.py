from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class TemperatureBase(BaseModel):
    id: int
    city_id: int
    data_time: Optional[datetime] = None
    temperature: int | float


class TemperatureUpdate(BaseModel):
    temperature: int | float


class Temperature(TemperatureBase):
    id: int
    city_id: int

    class Config:
        orm_mode = True
