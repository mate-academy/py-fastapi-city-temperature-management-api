from pydantic import BaseModel
from datetime import datetime
from typing import Optional, List

class TemperatureBase(BaseModel):
    temperature: float
    date_time: datetime

class Temperature(TemperatureBase):
    id: int
    city_id: int
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