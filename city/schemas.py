from typing import List

from pydantic import BaseModel

from temperature.schemas import Temperature


class CityBase(BaseModel):
    name: str
    additional_info: str

    model_config = {
        "from_attributes": True
    }


class CityCreate(CityBase):
    pass


class CityUpdate(CityBase):
    pass


class City(CityBase):
    id: int

    model_config = {
        "from_attributes": True
    }


class CityDetail(CityBase):
    id: int
    temperatures: List[Temperature] = []

    model_config = {
        "from_attributes": True
    }
