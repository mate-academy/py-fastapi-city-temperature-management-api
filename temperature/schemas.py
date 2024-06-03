from pydantic import BaseModel
from datetime import datetime


class TemperatureBase(BaseModel):
    date_time: datetime
    temperature: int


class TemperatureCreate(TemperatureBase):
    city_id: int


class TemperatureList(TemperatureBase):
    id: int
    city_id: int

    class Config:
        from_attributes = True
