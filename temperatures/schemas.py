import datetime

from pydantic import BaseModel, ConfigDict


class TemperatureBase(BaseModel):
    temperature: float
    city_id: int


class TemperatureCreate(TemperatureBase):
    pass


class TemperatureRead(TemperatureBase):
    id: int
    date_time: datetime.datetime

    model_config = ConfigDict(from_attributes=True)
