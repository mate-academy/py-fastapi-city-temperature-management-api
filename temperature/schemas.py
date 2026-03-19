from datetime import datetime

from pydantic import BaseModel, ConfigDict


class TemperatureBase(BaseModel):
    temperature: float
    date_time: datetime
    city_id: int


class Temperature(TemperatureBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class TemperatureCreate(TemperatureBase):
    pass
