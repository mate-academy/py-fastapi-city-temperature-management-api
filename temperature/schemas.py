from pydantic import BaseModel, ConfigDict
from datetime import datetime


class TemperatureBase(BaseModel):
    date_time: datetime
    temperature: float


class Temperature(TemperatureBase):
    id: int
    city_id: int

    model_config = ConfigDict(from_attributes=True)