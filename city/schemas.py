from typing import List

from pydantic import BaseModel

from temperature.schemas import Temperature


class CityBase(BaseModel):
    name: str
    additional_info: str

    class Config:
        from_attributes = True


class CityCreate(CityBase):
    pass


class CityUpdate(CityBase):
    pass


class City(CityBase):
    id: int

    class Config:
        orm_mode = True


class CityDetail(CityBase):
    id: int
    temperatures: List[Temperature] = []

    class Config:
        from_attributes = True
