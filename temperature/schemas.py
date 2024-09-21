from pydantic import BaseModel
from datetime import datetime


class TemperatureBase(BaseModel):
    date_time: datetime
    temperature: float
    city_id: int


class TemperatureCreate(TemperatureBase):
    pass


class TemperatureRead(TemperatureBase):
    id: int

    class Config:
        from_attributes = True
