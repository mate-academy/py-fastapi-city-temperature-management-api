from datetime import datetime, timezone
from typing import List

from pydantic import BaseModel, ConfigDict, field_validator


class TemperatureBase(BaseModel):
    city_id: int
    date_time: datetime
    temperature: float

    @field_validator("date_time")
    @classmethod
    def assume_utc(cls, value: datetime) -> datetime:
        # SQLite does not keep tz info; all stored times are UTC.
        if value.tzinfo is None:
            return value.replace(tzinfo=timezone.utc)
        return value


class TemperatureCreate(TemperatureBase):
    pass


class Temperature(TemperatureBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class FailedCity(BaseModel):
    city_id: int
    city_name: str
    reason: str


class TemperatureUpdateResult(BaseModel):
    updated: List[Temperature]
    failed: List[FailedCity]
