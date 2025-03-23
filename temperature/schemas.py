from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class TemperatureBase(BaseModel):
    date_time: Optional[datetime]
    temperature: float
    city_id: int


class TemperatureCreate(TemperatureBase):
    pass


class Temperature(TemperatureBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
