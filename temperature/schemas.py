from datetime import datetime
from pydantic import BaseModel


class TemperatureBase(BaseModel):
    temperature: float 


class TemperatureCreate(TemperatureBase):
    city_id: int


class TemperatureNested(TemperatureBase):
    id: int


class Temperature(TemperatureBase):
    id: int
    city_id: int
    date_time: datetime

    class Config:
        from_attributes = True
