from datetime import datetime

from pydantic import BaseModel


class TemperatureCreate(BaseModel):
    city_id: int
    date_time: datetime
    temperature: float


class Temperature(TemperatureCreate):
    id: int
