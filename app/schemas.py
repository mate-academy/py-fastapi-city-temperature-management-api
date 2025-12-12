from datetime import datetime
from typing import List, Optional

from pydantic import BaseModel, Field


class CityBase(BaseModel):
    name: str = Field(..., example="Paris")
    additional_info: Optional[str] = Field(None, example="Capital of France")


class CityCreate(CityBase):
    pass


class CityUpdate(BaseModel):
    name: Optional[str] = Field(None, example="Paris")
    additional_info: Optional[str] = Field(None, example="Capital of France")


class CityOut(CityBase):
    id: int

    class Config:
        orm_mode = True


class TemperatureBase(BaseModel):
    city_id: int
    temperature: float = Field(..., example=22.5)


class TemperatureCreate(TemperatureBase):
    date_time: datetime


class TemperatureOut(BaseModel):
    id: int
    city_id: int
    date_time: datetime
    temperature: float

    class Config:
        orm_mode = True


class TemperatureHistoryResponse(BaseModel):
    records: List[TemperatureOut]
    total: int


class TemperatureUpdateResult(BaseModel):
    inserted: int
    failed: int
    skipped: int
    message: str

