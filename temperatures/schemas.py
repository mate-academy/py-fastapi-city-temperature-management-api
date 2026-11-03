from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class TemperatureBase(BaseModel):
    temperature: float
    city_id: int


class TemperatureUpdate(BaseModel):
    temperature: Optional[float] = None
    city_id: Optional[int] = None


class Temperature(TemperatureBase):
    id: int
    date_time: datetime

    model_config = ConfigDict(from_attributes=True)
