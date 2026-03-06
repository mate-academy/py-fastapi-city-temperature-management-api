from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, ConfigDict


class TemperatureBase(BaseModel):
    city_id: int
    temperature: float = Field(..., description="Temperature value (e.g. °C)")


class TemperatureCreate(TemperatureBase):
    date_time: Optional[datetime] = None


class TemperatureRead(TemperatureBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    date_time: datetime
