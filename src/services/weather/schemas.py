from datetime import datetime, timezone

from pydantic import BaseModel, Field, field_validator


class WeatherData(BaseModel):
    temperature: float = Field(...)
    date_time: datetime = Field(...)

    @field_validator("date_time", mode="before")
    @classmethod
    def parse_last_updated(cls, v):
        if isinstance(v, datetime):
            return v
        if isinstance(v, (int, float)):
            return datetime.fromtimestamp(v, tz=timezone.utc)
        elif isinstance(v, str):
            return datetime.strptime(v, "%Y-%m-%d %H:%M")
        else:
            raise ValueError(f"Unsupported format for date_time: {v}")
