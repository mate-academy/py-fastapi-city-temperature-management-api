"""Request and response schemas."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


class CityBase(BaseModel):
    name: str = Field(min_length=1, max_length=120)
    additional_info: str | None = None

    @field_validator("name")
    @classmethod
    def normalize_name(cls, value: str) -> str:
        normalized = value.strip()
        if not normalized:
            raise ValueError("city name must not be blank")
        return normalized


class CityCreate(CityBase):
    pass


class CityUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=120)
    additional_info: str | None = None

    @field_validator("name")
    @classmethod
    def normalize_name(cls, value: str | None) -> str:
        if value is None:
            raise ValueError("city name must not be null")
        normalized = value.strip()
        if not normalized:
            raise ValueError("city name must not be blank")
        return normalized


class City(CityBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class Temperature(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    city_id: int
    date_time: datetime
    temperature: float
