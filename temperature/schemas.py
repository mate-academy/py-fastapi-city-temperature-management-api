import datetime

from pydantic import BaseModel

from city.schemas import City


class TemperatureBase(BaseModel):
    date_time: datetime.datetime
    temperature: int
    city_id: int


class Temperature(TemperatureBase):
    id: int
    city: City

    class Config:
        orm_mode = True
