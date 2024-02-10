from datetime import datetime

from pydantic import BaseModel


class TemperatureBase(BaseModel):
    date_time: datetime
    temperature: float
    city_id: int


class Temperature(BaseModel):
    temperature: float

    class Config:
        from_attributes = True


class TemperatureCity(TemperatureBase):

    class Config:
        from_attributes = True


class TemperatureUpdate(TemperatureBase):
    pass
