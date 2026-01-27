from datetime import datetime

from pydantic import BaseModel, ConfigDict


class TemperatureBase(BaseModel):
    date_time: datetime
    temperature: float
    city_id: int


class Temperature(TemperatureBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
