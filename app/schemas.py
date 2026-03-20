from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime


class CityBase(BaseModel):
    name: str = Field(..., examples=["London"])
    additional_info: Optional[str] = Field(None, examples=["Capital of Great Britain"])


class CityCreate(CityBase):
    pass


class CityUpdate(CityBase):
    pass


class City(CityBase):
    id: int

    class Config:
        from_attributes = True


class TemperatureBase(BaseModel):
    temperature: float


class TemperatureCreate(TemperatureBase):
    pass


class Temperature(TemperatureBase):
    id: int
    city_id: int
    date_time: datetime

    class Config:
        from_attributes = True
