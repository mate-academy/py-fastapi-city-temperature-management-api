from __future__ import annotations

import datetime
from pydantic import BaseModel, ConfigDict


class TemperatureBase(BaseModel):
    city_id: int
    temperature: float


class TemperatureRead(TemperatureBase):
    id: int
    date_time: datetime.datetime

    model_config = ConfigDict(from_attributes=True)


class TemperatureCreate(TemperatureBase):
    pass
