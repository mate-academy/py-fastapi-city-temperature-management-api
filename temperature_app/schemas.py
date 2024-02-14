from datetime import datetime

from pydantic import BaseModel


class Temperature(BaseModel):
    id: int
    city_id: int
    date_time: datetime
    temperature: float

    class Config:
        from_attributes = True


class TemperatureCreate(BaseModel):
    city_id: int
    date_time: datetime
    temperature: float
