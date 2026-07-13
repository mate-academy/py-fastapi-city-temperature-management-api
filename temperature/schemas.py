from datetime import datetime

from pydantic import BaseModel, ConfigDict


class TemperatureBase(BaseModel):
    city_id: int
    date_time: datetime
    temperature: float


class TemperatureResponse(TemperatureBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
