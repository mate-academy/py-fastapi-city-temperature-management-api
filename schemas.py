from pydantic import BaseModel, ConfigDict, Field
from datetime import datetime
from typing import List


class TemperatureBase(BaseModel):
    date_time: datetime
    temperature: float = Field(...)


class TemperatureCreate(TemperatureBase):
    city_id: int


class Temperature(TemperatureBase):
    id: int
    city_id: int

    model_config = ConfigDict(from_attributes=True)


class CityBase(BaseModel):
    name: str
    additional_info: str | None


class CityCreate(CityBase):
    pass

class City(CityBase):
    id: int
    temperature: List[Temperature] = []

    model_config = ConfigDict(from_attributes=True)

class CityOut(CityBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
