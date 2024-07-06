from datetime import datetime

from pydantic import BaseModel


class TemperatureBase(BaseModel):
    city_id: int
    date_time: datetime
    temperature: float


class TemperatureCreate(TemperatureBase):
    pass


class TemperatureUpdate(TemperatureBase):
    id: int


class TemperatureDelete(TemperatureBase):
    id: int


class Temperature(TemperatureBase):
    id: int

    class Config:
        from_attributes = True
