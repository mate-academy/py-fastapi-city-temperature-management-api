from pydantic import BaseModel
from datetime import datetime


class CityBase(BaseModel):
    name: str
    additional_info: str | None = None
    latitude: float
    longitude: float


class CityCreate(CityBase):
    pass


class City(CityBase):
    id: int

    class Config:
        orm_mode = True


class TemperatureBase(BaseModel):
    city_id: int
    temperature: float


class Temperature(TemperatureBase):
    id: int
    date_time: datetime

    class Config:
        orm_mode = True
