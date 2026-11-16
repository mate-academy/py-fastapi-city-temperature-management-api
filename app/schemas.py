"""Pydantic request and response schemas."""

from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field, field_validator


class CityBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    additional_info: str | None = None

    @field_validator("name")
    @classmethod
    def strip_city_name(cls, value: str) -> str:
        value = value.strip()
        if not value:
            raise ValueError("City name must not be blank")
        return value


class CityCreate(CityBase):
    """Fields accepted when creating a city."""


class CityUpdate(BaseModel):
    """Fields accepted when updating a city."""

    model_config = ConfigDict(extra="forbid")

    name: str | None = Field(default=None, min_length=1, max_length=100)
    additional_info: str | None = None

    @field_validator("name")
    @classmethod
    def strip_optional_city_name(cls, value: str | None) -> str | None:
        if value is None:
            return None
        value = value.strip()
        if not value:
            raise ValueError("City name must not be blank")
        return value


class CityRead(CityBase):
    """City returned by the API."""

    model_config = ConfigDict(from_attributes=True)

    id: int


class TemperatureRead(BaseModel):
    """Temperature history item returned by the API."""

    model_config = ConfigDict(from_attributes=True)

    id: int
    city_id: int
    date_time: datetime
    temperature: float


class TemperatureUpdateFailure(BaseModel):
    """A city whose current temperature could not be fetched."""

    city_id: int
    city_name: str
    reason: str


class TemperatureUpdateResult(BaseModel):
    """Summary of one update run."""

    updated_count: int
    failed_count: int
    failures: list[TemperatureUpdateFailure]

