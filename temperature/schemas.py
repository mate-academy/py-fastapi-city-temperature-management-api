import datetime

from pydantic import BaseModel, ConfigDict

from city.schemas import City


class TemperatureBase(BaseModel):
    temperature: float
    date_time: datetime.datetime


class Temperature(TemperatureBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    city: City
