from pydantic import BaseModel
from datetime import datetime


class TemperatureBase(BaseModel):
    city_id: int
    date_time: datetime
    temperature: float


class TemperatureCreate(TemperatureBase):
    pass


class TemperatureRead(TemperatureBase):
    id: int

    class Config:
        from_attributes = True
