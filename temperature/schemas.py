import datetime

from pydantic import BaseModel, ConfigDict


class TemperatureBase(BaseModel):
    temperature: float
    date_time: datetime


class TemperatureCreate(TemperatureBase):
    pass


class Temperature(TemperatureBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
