from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional

class TemperatureBase(BaseModel):
    date_time: datetime
    temperature: float


class TemperatureCreate(TemperatureBase):
    city_id: int


class Temperature(TemperatureBase):
    id: int
    city_id: int
    city: Optional['City'] = None

    class Config:
        from_attributes = True


class CityBase(BaseModel):
    name: str
    additional_info: Optional[str] = None


class CityCreate(CityBase):
    id: int


class City(CityBase):
    id: int
    temperatures: List[Temperature] = []

    class Config:
        from_attributes = True
