import datetime

from pydantic import BaseModel


class TemperatureBase(BaseModel):
    datetime: datetime.datetime
    temperature: float


class Temperature(TemperatureBase):
    id: int
    city_id: int

    class Config:
        from_attributes = True
