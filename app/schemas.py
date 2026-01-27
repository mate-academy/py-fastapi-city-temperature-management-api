from pydantic import BaseModel, Field, ConfigDict
from datetime import datetime
from typing import Optional


class CityBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100)
    additional_info: Optional[str] = None


class CityCreate(CityBase):
    pass


class CityUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=100)
    additional_info: Optional[str] = None


class City(CityBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


# Temperature schemas
class TemperatureBase(BaseModel):
    city_id: int
    temperature: float
    date_time: datetime


class TemperatureCreate(TemperatureBase):
    pass


class Temperature(TemperatureBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


class TemperatureUpdateResponse(BaseModel):
    message: str
    updated_count: int
    cities: list[str]
