from pydantic import BaseModel
from datetime import datetime


class BaseTemperature(BaseModel):
    city_id: int
    date_time: datetime
    temperature: float


class TemperatureCreate(BaseTemperature):
    pass


class Temperature(BaseTemperature):
    id: int

    class Config:
        from_attributes = True
