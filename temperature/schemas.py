from pydantic import BaseModel
from datetime import date


class TemperatureBase(BaseModel):
    city_id: int
    date_time: date
    temperature: str


class TemperatureCreate(TemperatureBase):
    pass


class TemperatureDefault(TemperatureBase):
    id: int

    class Config:
        orm_mode = True
