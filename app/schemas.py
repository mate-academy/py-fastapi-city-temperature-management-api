from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class CityBase(BaseModel):
    name: str
    additional_info: Optional[str] = None

    class Config:
        orm_mode = True


class CityCreate(CityBase):
    pass


class CityOut(CityBase):
    id: int

    class Config:
        orm_mode = True


class TemperatureBase(BaseModel):
    date_time: datetime
    temperature: float

    class Config:
        orm_mode = True


class TemperatureCreate(TemperatureBase):
    pass


class TemperatureOut(TemperatureBase):
    id: int
    city_id: int

    class Config:
        orm_mode = True

class TemperatureList(BaseModel):
    temperatures: List[TemperatureOut]
