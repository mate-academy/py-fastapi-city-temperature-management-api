import datetime

from pydantic import BaseModel, ConfigDict


class Temperature(BaseModel):
    temperature: float
    city_id: int


class TemperatureCreate(Temperature):
    pass


class TemperatureRead(Temperature):
    id: int
    date_time: datetime.datetime

    model_config = ConfigDict(from_attributes=True)
