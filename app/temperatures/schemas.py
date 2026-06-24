from pydantic import BaseModel, ConfigDict
from datetime import datetime


class TemperatureBase(BaseModel):
    temperature: float


class TemperatureCreate(TemperatureBase):
    city_id: int
    date_time: datetime


class Temperature(TemperatureBase):
    id: int
    city_id: int
    date_time: datetime

    model_config = ConfigDict(from_attributes=True)
