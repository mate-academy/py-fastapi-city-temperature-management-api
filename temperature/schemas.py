import datetime

from pydantic import BaseModel


class TemperatureBase(BaseModel):
    date_time: datetime.datetime
    temperature: float
    city_id: int


class Temperature(TemperatureBase):
    id: int
