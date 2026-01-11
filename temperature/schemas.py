import datetime

from pydantic import BaseModel, ConfigDict


class TemperatureBase(BaseModel):
    date_time: datetime.datetime
    temperature: float
    city_id: int


class TemperatureCreate(TemperatureBase):
    pass


class Temperature(TemperatureBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

