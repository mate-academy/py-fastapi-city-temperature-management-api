import datetime

from pydantic import BaseModel


class TemperatureBase(BaseModel):
    temperature: float | None
    date_time: datetime.datetime | None


class Temperature(TemperatureBase):
    id: int
    city_id: int

    class Config:
        orm_mode = True
