from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class TemperatureBase(BaseModel):
    city_id: int
    temperature: float
    date_time: datetime


class TemperatureCreate(TemperatureBase):
    pass


class TemperatureResponse(TemperatureBase):
    id: int

    model_config = {
        "from_attributes": True
    }


class TemperatureUpdate(BaseModel):
    city_id: Optional[int] = None
    temperature: Optional[float] = None
    date_time: Optional[datetime] = None
