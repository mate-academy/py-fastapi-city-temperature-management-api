from typing import List

from pydantic import BaseModel

from temperature.temp_schemass import Temperature


class CityBase(BaseModel):
    name: str
    additional_info: str


class City(CityBase):

    class Config:
        from_attribute = True


class CityDetail(CityBase):
    id: int
    temperatures: List[Temperature]

    class Config:
        from_attribute = True
