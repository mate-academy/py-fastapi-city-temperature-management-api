from datetime import datetime
from pydantic import BaseModel
from typing import Optional, List

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
    temperature: float

class TemperatureCreate(TemperatureBase):
    pass

class Temperature(TemperatureBase):
    id: int
    date_time: datetime
    class Config:
        orm_mode = True
