from datetime import datetime
from pydantic import BaseModel

from city.schemas import City


class TemperatureBaseSerializer(BaseModel):
    date_time: datetime
    temperature: str


class TemperatureCreateSerializer(TemperatureBaseSerializer):
    city_id: int


class TemperatureSerializer(TemperatureBaseSerializer):
    id: int
    city: City

    class Config:
        orm_mode = True
