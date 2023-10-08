from datetime import date

from pydantic import BaseModel


class TemperatureBase(BaseModel):
    temperature: float
    date_time: date
    city_id: int


class TemperatureUpdate(TemperatureBase):
    pass


class Temperature(TemperatureBase):
    id: int

    class Config:
        orm_mode = True


class TemperatureCity(TemperatureBase):

    class Config:
        orm_mode = True
