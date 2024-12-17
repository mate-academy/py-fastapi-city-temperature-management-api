from pydantic import BaseModel
from datetime import datetime
from typing import List, Any


class TemperatureBase(BaseModel):
    city_id: int
    date_time: datetime
    temperature: float


class TemperatureCreate(TemperatureBase):
    city: Any


class TemperatureResults(TemperatureBase):
    id: int


class TemperatureResultsResponse(BaseModel):
    message: str
    city: str
    temperatures: List[TemperatureResults]


class TemperatureUpdateResponse(BaseModel):
    message: str
    updated_records: int
    temperatures: List[TemperatureCreate]


class Temperature(TemperatureBase):
    id: int

    class Config:
        from_attributes = True
