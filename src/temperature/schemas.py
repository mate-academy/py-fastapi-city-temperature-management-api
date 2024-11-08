from datetime import datetime

from pydantic import BaseModel

from src.city.schemas import City


class BaseTemperature(BaseModel):
    ...


class Temperature(BaseTemperature):
    id: int
    date_time: datetime
    temperature: str
    city: City
