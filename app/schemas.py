from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class CityBase(BaseModel):
    name: str
    additional_info: Optional[str] = None


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

    class TemperatureCreate(BaseModel):
        city_id: int
        temperature: float


class Temperature(TemperatureBase):
    id: int

    class Config:
        orm_mode = True
