from datetime import datetime

from pydantic import BaseModel, ConfigDict


class TemperatureBase(BaseModel):
    city_id: int
    date_time: datetime
    temperature: float | int


class TemperatureCreate(TemperatureBase):
    pass


class Temperature(TemperatureBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class TemperatureUpdate(TemperatureBase):
    temperature_id: int | None
    city_id: int | None
    date_time: datetime | None

    model_config = ConfigDict(from_attributes=True)

