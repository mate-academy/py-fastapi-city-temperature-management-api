from datetime import datetime

from pydantic import BaseModel
from city import schemas


class TemperatureBase(BaseModel):
    date_time: datetime
    temperature: float
    city_id: int


class TemperatureCreate(TemperatureBase):
    pass


class TemperatureUpdate(BaseModel):
    message: str


class Temperature(TemperatureBase):
    id: int

    class Config:
        from_attributes = True
