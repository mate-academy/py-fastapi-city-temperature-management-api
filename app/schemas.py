from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, ConfigDict



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



class TemperatureBase(BaseModel):
    city_id: int
    temperature: float


class TemperatureCreate(TemperatureBase):
    date_time: datetime


class TemperatureResponse(TemperatureBase):
    id: int
    date_time: datetime

    model_config = ConfigDict(from_attributes=True)


class TemperatureUpdateResponse(BaseModel):
    updated_count: int
    records: List[TemperatureResponse]