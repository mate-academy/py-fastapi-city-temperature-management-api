from typing import Optional
from pydantic import BaseModel
from datetime import datetime


class CityBase(BaseModel):
    name: str
    additional_info: str
    latitude: float
    longitude: float


class CityCreate(CityBase):
    pass

class CityUpdate(CityBase):
    name: Optional[str] = None
    additional_info: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class City(BaseModel):
    id: int

    class Config:
        orm_mode = True

class Temperature(BaseModel):
    id: int
    city_id: int
    date_time: datetime
    temperature: float

    class Config:
        orm_mode = True