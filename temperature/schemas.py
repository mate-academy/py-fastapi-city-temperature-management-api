from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class TemperatureBase(BaseModel):
    temperature: float
    date_time: Optional[datetime] = None
    city_id: int


class TemperatureCreate(TemperatureBase):
    pass


class TemperatureResponse(TemperatureBase):
    id: int

    class Config:
        from_attributes = True
        