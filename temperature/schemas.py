from datetime import datetime

from pydantic import BaseModel, ConfigDict


class TemperatureBase(BaseModel):
    date_time: datetime
    temperature: float


class TemperatureCreate(TemperatureBase):
    pass


class TemperatureRead(TemperatureBase):
    id: int
    city_id: int

    model_config = ConfigDict(from_attributes=True)