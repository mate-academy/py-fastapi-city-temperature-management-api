from pydantic import BaseModel
from typing import Optional
from datetime import datetime


class CityCreate(BaseModel):
    name: str
    additional_info: Optional[str] = None


class CityOut(BaseModel):
    id: int
    name: str
    additional_info: Optional[str] = None

    class Config:
        from_orm_mode = True


class TemperatureCreate(BaseModel):
    city_id: int
    temperature: float


class TemperatureOut(BaseModel):
    id: int
    city_id: int
    date_time: datetime
    temperature: float

    class Config:
        from_orm_mode = True
