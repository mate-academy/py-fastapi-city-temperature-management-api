from datetime import datetime, timezone

from pydantic import BaseModel, Field, field_validator


class TemperatureData(BaseModel):
    temperature: float = Field(...)

class TemperatureRead(BaseModel):
    id: int
    city_id: int
    date_time: datetime
    temperature: float

    model_config = {
        "from_attributes": True
    }



class WeatherData(BaseModel):
    temp_c: float = Field(...)
    last_updated: datetime = Field(...)

    @field_validator("last_updated", mode="before")
    @classmethod
    def parse_last_updated(cls, v):
        if isinstance(v, datetime):
            return v
        if isinstance(v, (int, float)):
            return datetime.fromtimestamp(v, tz=timezone.utc)
        elif isinstance(v, str):
            return datetime.strptime(v, "%Y-%m-%d %H:%M")
        else:
            raise ValueError(f"Unsupported format for last_updated: {v}")