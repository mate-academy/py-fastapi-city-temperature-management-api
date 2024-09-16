from datetime import datetime

from pydantic import BaseModel


class TemperatureIn(BaseModel):
    date_time: datetime
    temperature: float


class Temperature(BaseModel):
    id: int
    date_time: datetime
    temperature: float
    city_id: int

    class Config:
        from_attributes = True
