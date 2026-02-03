from __future__ import annotations

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class CityBase(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    additional_info: Optional[str] = Field(default=None, max_length=2000)


class CityCreate(CityBase):
    pass


class CityUpdate(BaseModel):
    name: Optional[str] = Field(default=None, min_length=1, max_length=200)
    additional_info: Optional[str] = Field(default=None, max_length=2000)


class CityRead(CityBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class TemperatureRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    city_id: int
    date_time: datetime
    temperature: float


class TemperatureUpdateResult(BaseModel):
    created: int
    failed: int
    details: list[dict]
