from typing import List
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
        orm_mode = True


class TemperatureBase(BaseModel):
    city_id: int
    date_time: datetime
    temperature: float


class TemperatureCreate(TemperatureBase):
    pass


class Temperature(TemperatureBase):
    id: int

    class Config:
        orm_mode = True

class TemperatureUpdateDetail(BaseModel):
    city: str
    temperature: float

class TemperatureUpdateResponse(BaseModel):
    updated: int
    details: List[TemperatureUpdateDetail]