import datetime

from pydantic import BaseModel


class CityCreate(BaseModel):
    name: str
    additional_info: str


class City(CityCreate):
    id: int


class TemperatureCreate(BaseModel):
    city_id: int
    date_time: datetime.datetime
    temperature: float


class Temperature(TemperatureCreate):
    id: int
