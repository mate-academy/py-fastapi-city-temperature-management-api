from pydantic import BaseModel
from typing import List


class TemperatureBase(BaseModel):
    value: float
    unit: str


class TemperatureCreate(TemperatureBase):
    pass


class Temperature(TemperatureBase):
    id: int
    city_id: int

    class Config:
        orm_mode = True


class CityBase(BaseModel):
    name: str
    country: str


class CityCreate(CityBase):
    pass


class City(CityBase):
    id: int
    temperatures: List[Temperature] = []

    class Config:
        orm_mode = True
