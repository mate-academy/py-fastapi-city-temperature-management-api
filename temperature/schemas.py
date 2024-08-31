from datetime import datetime

from pydantic import BaseModel

from city.schemas import CityBase


class TemperatureBase(BaseModel):
    city_id: int
    date_time: datetime
    temperature: float

    class Config:
        from_attributes = True


class TemperatureCreate(TemperatureBase):
    pass


class Temperature(TemperatureBase):
    id: int
    city: CityBase

    class Config:
        from_attributes = True
