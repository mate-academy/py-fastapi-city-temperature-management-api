from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class CityBase(BaseModel):
    name: str
    additional_info: Optional[str]


class CityCreate(CityBase):
    pass


class City(CityBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class CityUpdate(CityBase):
    name: str
    additional_info: str
    model_config = ConfigDict(from_attributes=True)


class TemperatureBase(BaseModel):
    date_time: datetime
    temperature: float


class TemperatureCreate(TemperatureBase):
    city_id: int
    pass


class Temperature(TemperatureBase):
    id: int
    city: City
    model_config = ConfigDict(from_attributes=True)


class TemperatureUpdate(TemperatureBase):
    date_time: Optional[datetime]
    temperature: Optional[float]
    model_config = ConfigDict(from_attributes=True)
