import datetime

from pydantic import BaseModel, ConfigDict
from pydantic.v1 import Field


class CityBase(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    country: str = Field(min_length=1, max_length=255)
    additional_info: str | None = None


class CityCreate(CityBase):
    pass


class City(CityBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class TemperatureBase(BaseModel):
    city_id: int
    temperature: float


class Temperature(BaseModel):
    id: int
    date_time: datetime.datetime
    temperature: float
    city: City

    model_config = ConfigDict(from_attributes=True)
