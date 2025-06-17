from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict

from city.schemas import City


class TemperatureBase(BaseModel):
    temperature: float
    date_time: datetime

    model_config = ConfigDict(arbitrary_types_allowed=True)


class TemperatureCreate(TemperatureBase):
    city_id: int


class TemperatureUpdate(TemperatureBase):
    pass


class Temperature(TemperatureBase):
    id: int

    class Config:
        from_attributes = True
