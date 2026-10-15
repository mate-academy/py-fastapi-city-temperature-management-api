from datetime import datetime, timezone

from pydantic import BaseModel, ConfigDict, field_validator


class TemperatureSchema(BaseModel):
    id: int
    city_id: int
    date_time: datetime
    temperature: float

    model_config = ConfigDict(from_attributes=True)

    @field_validator("date_time")
    @classmethod
    def set_utc_timezone(cls, value: datetime) -> datetime:
        # SQLite does not store timezone, so naive values are UTC
        if value.tzinfo is None:
            return value.replace(tzinfo=timezone.utc)
        return value


class TemperatureUpdateError(BaseModel):
    city: str
    error: str


class TemperatureUpdateResult(BaseModel):
    updated: list[str]
    failed: list[TemperatureUpdateError]
