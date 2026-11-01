from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CityCreate(BaseModel):
    name: str
    additional_info: str | None = None


class CityResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    additional_info: str | None = None


class TemperatureResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    city_id: int
    date_time: datetime
    temperature: float


class TemperatureCreate(BaseModel):
    city_id: int
    date_time: datetime
    temperature: float
