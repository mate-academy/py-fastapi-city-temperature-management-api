from datetime import datetime
from pydantic import BaseModel, ConfigDict


class TemperatureBase(BaseModel):
    city_id: int
    temperature: float


class TemperatureCreate(TemperatureBase):
    date_time: datetime


class Temperature(TemperatureBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    date_time: datetime
