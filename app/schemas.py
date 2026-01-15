from typing import Optional
from pydantic import BaseModel, ConfigDict
from datetime import datetime


class CityBase(BaseModel):
    name: str
    additional_info: Optional[str]


class CityCreate(CityBase):
    pass


class City(CityBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class CityUpdate(CityBase):
    pass


class TemperatureBase(BaseModel):
    date_time: datetime
    temperature: float


class TemperatureList(TemperatureBase):
    id: int
    city_id: int

    model_config = ConfigDict(from_attributes=True)


class TemperatureDetail(TemperatureBase):
    city: City
