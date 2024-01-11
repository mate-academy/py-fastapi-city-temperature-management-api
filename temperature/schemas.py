from pydantic import BaseModel

from datetime import datetime
from city.schemas import City


class TemperatureBase(BaseModel):
    date_time: datetime = datetime.now()
    temperature: float


class TemperatureCreate(TemperatureBase):
    city_id: int


class Temperature(TemperatureBase):
    id: int
    city_id: int

    class Config:
        from_attributes = True
