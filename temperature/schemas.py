from datetime import datetime
from pydantic import BaseModel, ConfigDict


class TemperatureBase(BaseModel):
    city_id: int
    date_time: datetime
    temperature: float


class Temperature(TemperatureBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
