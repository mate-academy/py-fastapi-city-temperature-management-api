from datetime import datetime

from pydantic import BaseModel, ConfigDict


class TemperatureBase(BaseModel):
    temperature: float
    date_time: datetime
    city_id: int


class TemperatureList(TemperatureBase):
    pass


class Temperature(TemperatureBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


class TemperatureCreate(TemperatureBase):
    pass
