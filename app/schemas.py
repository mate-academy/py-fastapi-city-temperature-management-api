from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class CityBase(BaseModel):
    name: str
    additional_info: Optional[str] = None

class CityCreate(CityBase):
    pass

class CityRead(CityBase):
    id: int
    class Config:
        orm_mode = True


class City(CityRead):
    pass

class TemperatureBase(BaseModel):
    city_id: int
    temperature: float
    date_time: Optional[datetime] = None

class TemperatureCreate(TemperatureBase):
    pass

class TemperatureRead(TemperatureBase):
    id: int
    date_time: datetime
    class Config:
        orm_mode = True

