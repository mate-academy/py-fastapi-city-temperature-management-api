from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel


class TemperatureBase(BaseModel):
    temperature: float


class TemperatureCreate(TemperatureBase):
    city_id: int
    date_time: datetime


class TemperatureResponse(TemperatureBase):
    id: int
    city_id: int
    date_time: datetime

    class Config:
        from_attributes = True


class CityBase(BaseModel):
    name: str
    additional_info: Optional[str] = None


class CityCreate(CityBase):
    pass


class CityUpdate(CityBase):
    pass


class CityResponse(CityBase):
    id: int

    class Config:
        from_attributes = True
