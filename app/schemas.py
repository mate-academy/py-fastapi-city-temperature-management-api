from datetime import datetime
from typing import List

from pydantic import BaseModel, ConfigDict


class CityBase(BaseModel):
    name: str
    additional_info: str


class CityCreate(CityBase):
    pass


class CityResponse(CityBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class TemperatureBase(BaseModel):
    city_id: int
    date_time: datetime
    temperature: float


class TemperatureCreate(TemperatureBase):
    pass


class TemperatureResponse(TemperatureBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class SuccessUpdate(BaseModel):
    city: str
    temperature: float


class FailedUpdate(BaseModel):
    city: str
    error: str


class TemperatureUpdateResponse(BaseModel):
    success_cities: List[SuccessUpdate]
    failed_cities: List[FailedUpdate]
