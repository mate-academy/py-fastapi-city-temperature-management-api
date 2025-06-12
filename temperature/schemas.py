from pydantic import BaseModel
import datetime


class TemperatureBase(BaseModel):
    date_time: datetime.datetime
    temperature: float


class TemperatureCreate(TemperatureBase):
    city_id: int


class Temperature(TemperatureBase):
    id: int

    class Config:
        orm_mode = True
