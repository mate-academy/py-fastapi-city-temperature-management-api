from datetime import datetime, timezone

from pydantic import BaseModel, ConfigDict, field_validator


class TemperatureRequestSchema(BaseModel):
    temperature: float


class TemperatureCreateSchema(TemperatureRequestSchema):
    city_id: int


class TemperatureResponseSchema(TemperatureRequestSchema):
    id: int
    city_id: int
    date_time: datetime

    model_config = ConfigDict(from_attributes=True)

    @field_validator("date_time")
    @classmethod
    def validate_date_time(cls, value):
        if value.tzinfo is None:
            value = value.replace(tzinfo=timezone.utc)
        if value > datetime.now(timezone.utc):
            raise ValueError("date_time cannot be in the future")
        return value


class PaginatedTemperatureResponseSchema(BaseModel):
    temperatures: list[TemperatureResponseSchema]
    total_items: int
    total_pages: int
    prev_page: str | None = None
    next_page: str | None = None

    model_config = ConfigDict(from_attributes=True)
