from datetime import datetime

from pydantic import BaseModel

from city_app.schemas import CityBase


class TemperatureBase(BaseModel):
    city_id: int
    date_time: datetime
    temperature: float


class TemperatureCreate(TemperatureBase):
    pass


class TemperatureList(TemperatureBase):
    id: int
    city: CityBase

    class Config:
        from_attributes = True
