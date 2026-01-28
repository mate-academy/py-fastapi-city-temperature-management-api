from datetime import datetime
from pydantic import BaseModel, Field


# ---------- City ----------
class CityBase(BaseModel):
    name: str = Field(..., min_length=1)
    additional_info: str | None = None


class CityCreate(CityBase):
    pass


class CityUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1)
    additional_info: str | None = None


class CityRead(CityBase):
    id: int

    model_config = {"from_attributes": True}


# ---------- Temperature ----------
class TemperatureRead(BaseModel):
    id: int
    city_id: int
    date_time: datetime
    temperature: float

    model_config = {"from_attributes": True}


class TemperatureUpdateResult(BaseModel):
    city_id: int
    city_name: str
    ok: bool
    temperature: float | None = None
    error: str | None = None
