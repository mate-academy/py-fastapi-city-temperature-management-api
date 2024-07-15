from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class CityBase(BaseModel):
    name: str
    additional_info: Optional[str] = None


class CityCreate(CityBase):
    pass


class City(CityBase):
    id: int
    temperatures: List["Temperature"] = []

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True


class TemperatureBase(BaseModel):
    city_id: int
    date_time: datetime
    temperature: float


class TemperatureCreate(TemperatureBase):
    pass


class Temperature(TemperatureBase):
    id: int

    class Config:
        from_attributes = True
        arbitrary_types_allowed = True
