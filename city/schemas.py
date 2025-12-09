from typing import List

from pydantic import BaseModel

from temperature.schemas import TemperatureSchema


class CitySchema(BaseModel):
    name: str
    additional_info: str

    model_config = {
        "from_attributes": True
    }


class CityCreateSchema(CitySchema):
    pass


class CityListSchema(BaseModel):
    id: int
    name: str

    model_config = {
        "from_attributes": True
    }


class CityDetailSchema(CityListSchema):
    temperatures: List[TemperatureSchema]

    model_config = {
        "from_attributes": True
    }


class CityUpdateSchema(CitySchema):
    id: int
