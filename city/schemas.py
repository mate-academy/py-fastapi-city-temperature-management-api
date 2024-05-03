from typing import List

from pydantic import BaseModel

from temperature.schemas import TemperatureSchema


class CityBase(BaseModel):
    name: str
    additional_info: str


class CitySchema(CityBase):

    class Config:
        from_attribute = True


class CityDetail(CityBase):
    id: int
    temperatures: List[TemperatureSchema]

    class Config:
        from_attribute = True
