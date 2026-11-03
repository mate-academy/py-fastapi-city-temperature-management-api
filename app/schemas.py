from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional


class CityBase(BaseModel):
    name: str
    additional_info: Optional[str] = None


class CityCreate(CityBase):
    pass


class CityUpdate(CityBase):
    pass


class City(CityBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class TemperatureBase(BaseModel):
    city_id: int
    temperature: float


class TemperatureCreate(TemperatureBase):
    date_time: Optional[datetime] = None


class Temperature(TemperatureBase):
    id: int
    date_time: datetime

    model_config = ConfigDict(from_attributes=True)
