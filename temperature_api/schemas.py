from pydantic import BaseModel
from datetime import datetime


class Temperature(BaseModel):
    id: int
    city_id: int
    date_time: datetime
    temperature: float

    class Config:
        from_attributes = True


class TemperatureCreate(BaseModel):
    city_id: int
    date_time: datetime
    temperature: float


class TemperatureList(BaseModel):
    temperature_list: list[Temperature]


class TemperatureRead(BaseModel):
    city_id: int
    date_time: datetime
    temperature: float
