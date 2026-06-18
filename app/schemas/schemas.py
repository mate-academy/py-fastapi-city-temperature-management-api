from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


# ──────────────────────────────────────────────────────────────
#  City schemas
# ──────────────────────────────────────────────────────────────

class CityBase(BaseModel):
    name: str = Field(..., min_length=1, description="Name of the city")
    additional_info: Optional[str] = Field(None, description="Any extra info about the city")


class CityCreate(CityBase):
    """Schema used when creating a new city (request body)."""
    pass


class CityUpdate(BaseModel):
    """Schema used when updating a city (all fields optional)."""
    name: Optional[str] = Field(None, min_length=1)
    additional_info: Optional[str] = None


class CityResponse(CityBase):
    """Schema returned to the client for city data."""
    id: int

    model_config = {"from_attributes": True}


# ──────────────────────────────────────────────────────────────
#  Temperature schemas
# ──────────────────────────────────────────────────────────────

class TemperatureBase(BaseModel):
    city_id: int
    date_time: datetime
    temperature: float = Field(..., description="Temperature in Celsius")


class TemperatureResponse(TemperatureBase):
    """Schema returned to the client for temperature records."""
    id: int

    model_config = {"from_attributes": True}


class TemperatureUpdateResponse(BaseModel):
    """Summary response after a bulk temperature update."""
    updated: int = Field(..., description="Number of cities successfully updated")
    failed: int = Field(..., description="Number of cities that could not be fetched")
    records: list[TemperatureResponse] = Field(default_factory=list)