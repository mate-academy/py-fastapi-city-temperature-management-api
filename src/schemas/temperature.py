from datetime import datetime
from decimal import Decimal

from pydantic import BaseModel, Field, ConfigDict

NOW_FACTORY = datetime.now


class TemperatureBase(BaseModel):
    temperature: Decimal
    city_id: int


class TemperatureCreate(TemperatureBase):
    pass


class TemperatureRead(TemperatureBase):
    id: int
    date_time: datetime = Field(default_factory=NOW_FACTORY)

    model_config = ConfigDict(from_attributes=True)
