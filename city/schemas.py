from typing import List

from pydantic import BaseModel

from temperature.schemas import Temperature


class CityBase(BaseModel):
    name: str


class CityCreate(CityBase):
    additional_info: str


class City(CityBase):
    id: int

    class Config:
        from_attributes = True


class CityDetail(CityBase):
    id: int
    additional_info: str
    temperatures: List[Temperature] = []

    class Config:
        from_attributes = True


class CityUpdate(CityBase):
    additional_info: str
