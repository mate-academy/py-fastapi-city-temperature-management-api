"""Pydantic schemas used for request validation and response serialization."""
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


# ---------------------------------------------------------------------------
# City schemas
# ---------------------------------------------------------------------------
class CityBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, description="City name")
    additional_info: Optional[str] = Field(
        None, description="Any extra information about the city"
    )


class CityCreate(CityBase):
    """Payload for POST /cities. `id` is assigned by the database."""


class CityUpdate(BaseModel):
    """Payload for PUT /cities/{city_id}. All fields optional (partial update)."""

    name: Optional[str] = Field(None, min_length=1, max_length=100)
    additional_info: Optional[str] = None


class City(CityBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


# ---------------------------------------------------------------------------
# Temperature schemas
# ---------------------------------------------------------------------------
class TemperatureBase(BaseModel):
    city_id: int
    date_time: datetime
    temperature: float


class Temperature(TemperatureBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class TemperatureUpdateResult(BaseModel):
    """Summary returned by POST /temperatures/update."""

    updated: list[Temperature]
    failed: list[dict] = Field(
        default_factory=list,
        description="Cities whose temperature could not be fetched, with the reason",
    )
