from datetime import datetime

from pydantic import BaseModel


class TemperatureBase(BaseModel):
    city_id: int
    date_time: datetime
    temperature: float


class TemperatureCreate(TemperatureBase):
    id: int


class Temperature(BaseModel):
    id: int
    city_id: int
    date_time: datetime
    temperature: float

    class Config:
        orm_mode = True
