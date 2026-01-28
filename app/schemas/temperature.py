from datetime import datetime

from pydantic import BaseModel, ConfigDict


class TemperatureBase(BaseModel):
    city_id: int
    temperature: float


class TemperatureCreate(TemperatureBase):
    pass


class TemperatureRead(TemperatureBase):
    id: int
    date_time: datetime

    model_config = ConfigDict(from_attributes=True)
