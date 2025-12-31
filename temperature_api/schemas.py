import datetime
from typing import Union
from pydantic import BaseModel, ConfigDict


class TemperatureValue(BaseModel):
    temperature: Union[int, float]
    date_time: datetime.datetime


class Temperature(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    city_id: int
    date_time: datetime.datetime
    temperature: Union[int, float]

