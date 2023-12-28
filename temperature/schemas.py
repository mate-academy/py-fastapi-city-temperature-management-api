import datetime
from pydantic import BaseModel


class Temperature(BaseModel):
    id: int
    city_id: int
    date_time: datetime.datetime
    temperature: float


class TemperatureCreate(BaseModel):
    city_id: int
    date_time: datetime.datetime
    temperature: float
