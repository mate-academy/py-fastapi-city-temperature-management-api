from pydantic import BaseModel
from city.schemas import CityBase
from datetime import datetime


class TemperatureBase(BaseModel):
    city_id: int
    temperature: float


class TemperetureCreate(TemperatureBase):
    pass


class Tempereture(TemperatureBase):
    id: int
    city: CityBase
    date_time: datetime

    class Config:
        from_attributes = True
