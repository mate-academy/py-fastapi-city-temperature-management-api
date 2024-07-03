from datetime import datetime
from typing import List

from pydantic import BaseModel


class CityBase(BaseModel):
    name: str
    additional_info: str


class CityCreate(CityBase):
    pass


class CityUpdate(CityBase):
    pass


class City(CityBase):
    id: int
    temperatures: List["Temperature"] = []

    class Config:
        orm_mode = True


class TemperatureBase(BaseModel):
    date_time: datetime
    temperature: float


class TemperatureCreate(TemperatureBase):
    city_id: int


class TemperatureUpdate(TemperatureBase):
    pass


class Temperature(TemperatureBase):
    id: int
    city_id: City

    class Config:
        orm_mode = True
