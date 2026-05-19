from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class TemperatureBase(BaseModel):
    temperature: float
    city_id: int


class Temperature(TemperatureBase):
    id: int
    date_time: datetime

    class Config:
        from_attributes = True


class CityBase(BaseModel):
    name: str
    additional_info: Optional[str] = None


class CityCreate(CityBase):
    pass


class City(CityBase):
    id: int

    class Config:
        from_attributes = True
