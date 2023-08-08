from datetime import datetime

from pydantic import BaseModel

from cities.schemas import City


class BaseTemperature(BaseModel):
    city_id: int
    date_time: datetime
    temperature: float


class CreateTemperature(BaseTemperature):
    pass


class Temperature(BaseTemperature):
    id: int
    city: City

    class Config:
        orm_mode = True
