from pydantic import BaseModel
from datetime import datetime


class TemperatureRead(BaseModel):
    id: int
    city_id: int
    date_time: datetime
    temperature: int | float


class TemperatureCreate(BaseModel):
    city_id: int
    date_time: datetime
    temperature: int | float
