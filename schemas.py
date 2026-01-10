from typing import Optional

from pydantic import BaseModel

from datetime import datetime


class CityBase(BaseModel):
    name: str
    additional_info: str


class CityCreate(CityBase):
    pass

class City(CityBase):
    id: int

    class Config:
        from_attributes = True

class CityUpdate(BaseModel):
    name: Optional[str] = None
    additional_info: Optional[str] = None


class TemperatureBase(BaseModel):
    date_time: datetime
    temperature: float
    city_id: int


class TemperatureCreate(TemperatureBase):
    pass

class Temperature(TemperatureBase):
    id: int

    class Config:
        from_attributes = True
