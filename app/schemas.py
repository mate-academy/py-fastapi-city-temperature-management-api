from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class CityBase(BaseModel):
    name: str
    additional_info: Optional[str] = None


class CityCreate(CityBase):
    pass


class CityRead(CityBase):
    id: int

    class Config:
        orm_mode = True


class TemperatureBase(BaseModel):
    city_id: int
    temperature: float
    date_time: datetime


class TemperatureCreate(BaseModel):
    city_id: int
    temperature: float


class TemperatureRead(TemperatureBase):
    id: int

    class Config:
        orm_mode = True