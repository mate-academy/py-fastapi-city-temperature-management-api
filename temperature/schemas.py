from datetime import datetime

from pydantic import BaseModel


class TemperatureBase(BaseModel):
    city_id: int


class TemperatureCreate(TemperatureBase):
    pass


class Temperature(TemperatureBase):
    id: int
    temperature: float | None
    date_time: datetime | None

    class Config:
        orm_mode = True
