from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


# Temperature
class TemperatureBase(BaseModel):
    temperature: float


class TemperatureCreate(TemperatureBase):
    city_id: int


class Temperature(TemperatureBase):
    id: int
    city_id: int
    date_time: datetime

    model_config = ConfigDict(from_attributes=True)


# City
class CityBase(BaseModel):
    name: str
    additional_info: Optional[str] = None


class CityCreate(CityBase):
    pass


class CityUpdate(BaseModel):
    name: Optional[str] = None
    additional_info: Optional[str] = None


class City(CityBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
