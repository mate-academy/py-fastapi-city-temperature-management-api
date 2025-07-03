from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class CityBase(BaseModel):
    name: str
    additional_info: Optional[str] = None


class CityCreate(BaseModel):
    name: str
    additional_info: Optional[str] = None


class City(CityBase):
    id: int

    class Config:
        from_attributes = True


class TemperatureBase(BaseModel):
    city_id: int
    temperature: float


class TemperatureCreate(TemperatureBase):
    pass


class Temperature(TemperatureBase):
    id: int
    date_time: datetime

    class Config:
        from_attributes = True