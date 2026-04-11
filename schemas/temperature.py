from pydantic import BaseModel, ConfigDict
from datetime import datetime


class TemperatureBase(BaseModel):
    city_id: int
    datetime: datetime
    temperature: float


class TemperatureRead(TemperatureBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
