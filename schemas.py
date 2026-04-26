from typing import Optional
from datetime import datetime
from pydantic import BaseModel, ConfigDict


class CityBase(BaseModel):
    name: str
    additional_info: str


class CityCreate(CityBase):
    pass


class CityResponse(CityBase):
    id: int
    temperatures: list[TemperatureResponse]

    model_config = ConfigDict(from_attributes=True)


class CityUpdate(CityBase):
    name: Optional[str] = None
    additional_info: Optional[str] = None


class TemperatureBase(BaseModel):
    city_id: int
    date_time: datetime
    temperature: float


class TemperatureCreate(TemperatureBase):
    pass


class TemperatureResponse(TemperatureBase):
    id: int

    model_config = ConfigDict(from_attributes=True)