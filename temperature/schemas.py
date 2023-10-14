from datetime import datetime

from pydantic import BaseModel


class TemperatureBase(BaseModel):
    date_time: datetime
    temperature: int
    city_id: int


class TemperatureUpdate(TemperatureBase):
    pass


class Temperature(BaseModel):
    temperature: int

    class Config:
        from_attributes = True


class TemperatureCity(TemperatureBase):

    class Config:
        orm_mode = True