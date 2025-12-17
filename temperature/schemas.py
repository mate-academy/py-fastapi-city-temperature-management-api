from datetime import datetime

from pydantic import BaseModel


class TemperatureBase(BaseModel):
    city_id: int
    date_time: datetime | None = None
    temperature: float

class Temperature(TemperatureBase):
    id: int

    class Config:
        orm_mode = True


class TemperatureCreate(TemperatureBase):
    pass