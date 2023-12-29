from datetime import datetime
from pydantic import BaseModel


class TemperatureBase(BaseModel):
    temperature: float
    city_id: int


class TemperatureCreate(TemperatureBase):
    pass


class TemperatureList(TemperatureBase):
    id: int
    date_time: datetime

    class Config:
        orm_mode = True
