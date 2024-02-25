import datetime

from pydantic import BaseModel


class TemperatureBase(BaseModel):
    city_id: int
    date_time: datetime.datetime
    temperature: float


class TemperatureList(TemperatureBase):
    id: int

    class Config:
        from_attributes = True
