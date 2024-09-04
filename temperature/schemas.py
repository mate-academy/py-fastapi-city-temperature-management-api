import datetime

from pydantic import BaseModel
from city import schemas as city_schema


class TemperatureBase(BaseModel):
    temperature: float


class TemperatureCreate(TemperatureBase):
    city_id: int


class Temperature(TemperatureBase):
    id: int
    date_time: datetime.datetime
    city: city_schema.City

    class Config:
        orm_mode = True
