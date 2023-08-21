from pydantic import BaseModel

from cities.schemas import CityBase


class TemperatureBase(BaseModel):
    temperature: float
    date_time: str


class TemperatureCreate(TemperatureBase):
    city_id: int


class Temperature(TemperatureBase):
    id: int
    city: CityBase

    class Config:
        from_attributes = True
