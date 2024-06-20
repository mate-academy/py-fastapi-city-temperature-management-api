from datetime import datetime

from pydantic import BaseModel

from city.schemas import City


class TemperatureBase(BaseModel):
    date_time: datetime
    temperature: int


class TemperatureCreate(TemperatureBase):
    city_id: int


class TemperatureUpdate(TemperatureBase):
    pass


class Temperature(TemperatureBase):
    id: int
    city: City

    class Config:
        orm_mode = True
