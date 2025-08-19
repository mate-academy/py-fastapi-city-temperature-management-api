from datetime import datetime
from typing import List

from pydantic import BaseModel, ConfigDict


class TemperatureBase(BaseModel):
    city_id: int
    date_time: datetime
    temperature: float

    model_config = ConfigDict(from_attributes=True)


class TemperatureResponse(TemperatureBase):
    id: int


class TemperatureListResponse(BaseModel):
    temperatures: List[TemperatureResponse]
