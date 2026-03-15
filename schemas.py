from pydantic import BaseModel, Field
from datetime import datetime
from typing import List, Optional


class TemperatureBase(BaseModel):
    temperature: float

class Temperature(TemperatureBase):
    id: int
    city_id: int
    date_time: datetime

    class Config:
        from_attributes = True

class CityBase(BaseModel):
    name: str = Field(..., min_length=1)
    additional_info: Optional[str] = None
    latitude: float
    longitude: float

class CityCreate(CityBase):
    pass

class City(CityBase):
    id: int
    temperatures: List[Temperature] = []

    class Config:
        from_attributes = True
