from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class CityBase(BaseModel):
    name: str
    additional_info: Optional[str] = None


class CityCreate(CityBase):
    pass


class CityUpdate(BaseModel):
    name: Optional[str] = None
    additional_info: Optional[str] = None


class CityRead(CityBase):
    id: int

    class Config:
        orm_mode = True


class TemperatureBase(BaseModel):
    city_id: int
    date_time: datetime
    temperature: float


class TemperatureCreate(BaseModel):
    city_id: int
    temperature: float


class TemperatureRead(TemperatureBase):
    id: int

    class Config:
        orm_mode = True
