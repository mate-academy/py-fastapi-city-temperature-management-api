from pydantic import BaseModel

import datetime


class TemperatureBase(BaseModel):
    date_time: datetime.datetime | None = None
    temperature: float

    class Config:
        from_attributes = True


class TemperatureCreate(TemperatureBase):
    city_id: int


class Temperature(TemperatureBase):
    id: int
    city_id: int
