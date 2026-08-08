from datetime import datetime
from typing import Optional
from pydantic import BaseModel

class CityBase(BaseModel):
    name: str
    additional_info: Optional[str] = None

class CityCreate(CityBase):
    pass

class CityUpdate(BaseModel):
    name: Optional[str] = None
    additional_info: Optional[str] = None

class City(CityBase):
    id: int

    class Config:
        from_attributes = True

class TemperatureBase(BaseModel):
    temperature: float
    date_time: datetime  # Имя поля строго date_time

class TemperatureCreate(TemperatureBase):
    city_id: int

class Temperature(TemperatureBase):
    id: int
    city_id: int

    class Config:
        from_attributes = True