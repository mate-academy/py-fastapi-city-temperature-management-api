from typing import List

from pydantic import BaseModel


class City(BaseModel):
    id: int
    name: str
    additional_info: str

    class Config:
        from_attributes = True


class CityCreate(BaseModel):
    name: str
    additional_info: str


class CityRead(City):
    class Config:
        from_attributes = True


class CityList(BaseModel):
    cities: List[CityRead]

    class Config:
        from_attributes = True


class CityUpdate(CityCreate):
    pass
