from pydantic import BaseModel
from datetime import datetime


class TemperatureCreate(BaseModel):
    city_id: int
    date_time: datetime
    temperature: float


class TemperatureRead(BaseModel):
    id: int
    city_id: int
    date_time: datetime
    temperature: float

    class Config:
        orm_mode = True
