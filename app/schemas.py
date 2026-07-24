from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


# --- City Schemas ---
class CityBase(BaseModel):
    name: str
    additional_info: Optional[str] = None


class CityCreate(CityBase):
    pass


class CityUpdate(BaseModel):
    name: Optional[str] = None
    additional_info: Optional[str] = None


class CityResponse(CityBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


# --- Temperature Schemas ---
class TemperatureResponse(BaseModel):
    id: int
    city_id: int
    date_time: datetime
    temperature: float

    model_config = ConfigDict(from_attributes=True)


class TemperatureUpdateSummary(BaseModel):
    updated_count: int
    failed_cities: list[str]
