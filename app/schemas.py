from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CityBase(BaseModel):
    name: str
    additional_info: str | None = None


class CityCreate(CityBase):
    pass


class CityUpdate(BaseModel):
    name: str | None = None
    additional_info: str | None = None


class City(CityBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class TemperatureBase(BaseModel):
    city_id: int
    temperature: float


class TemperatureCreate(TemperatureBase):
    pass


class Temperature(TemperatureBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    date_time: datetime


class TemperatureUpdateResult(BaseModel):
    updated: list[Temperature]
    errors: list[str] = []
