from datetime import datetime
from typing import Optional
from pydantic import BaseModel, Field


# ----- City Schemas -----
class CityBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=255)
    additional_info: Optional[str] = Field(None, max_length=1024)


class CityCreate(CityBase):
    pass


class CityUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, max_length=255)
    additional_info: Optional[str] = Field(None, max_length=1024)


class CityOut(CityBase):
    id: int

    class Config:
        from_attributes = True


# ----- Temperature Schemas -----
class TemperatureBase(BaseModel):
    city_id: int
    temperature: float


class TemperatureCreate(TemperatureBase):
    date_time: Optional[datetime] = None


class TemperatureOut(BaseModel):
    id: int
    city_id: int
    date_time: datetime
    temperature: float

    class Config:
        from_attributes = True
