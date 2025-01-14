from datetime import datetime

from pydantic import BaseModel

class TemperatureBase(BaseModel):
    temperature: float
    date_time: datetime


class TemperatureCreate(TemperatureBase):
    pass

class Temperature(TemperatureBase):
    id: int

    class Config:
        orm_mode = True
