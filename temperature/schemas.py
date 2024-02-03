import datetime
from _decimal import Decimal

from pydantic import BaseModel


class TemperatureBase(BaseModel):
    date_time: datetime.datetime
    temperature_indicator: Decimal


class Temperature(TemperatureBase):
    id: int
    city_id: int

    class Config:
        from_attributes = True
