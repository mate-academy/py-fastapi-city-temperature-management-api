from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class TemperatureBase(BaseModel):
    date_time: datetime
    temperature: float


class TemperatureCreate(TemperatureBase):
    city_id: int
    date_time: datetime


class TemperatureUpdate(BaseModel):
    date_time: Optional[datetime] = None
    temperature: Optional[float] = None

    model_config = ConfigDict(from_attributes=True)


class Temperature(TemperatureBase):
    id: int
    city_id: int

    model_config = ConfigDict(from_attributes=True)
