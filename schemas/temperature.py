from datetime import datetime

from pydantic import BaseModel, ConfigDict


class TemperatureBase(BaseModel):
    city_id: int
    date_time: datetime
    temperature: float


class TemperatureCreate(TemperatureBase):
    pass


class Temperature(TemperatureBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class TemperatureUpdateError(BaseModel):
    city_id: int
    city_name: str
    detail: str


class TemperatureUpdateResult(BaseModel):
    updated: list[Temperature]
    failed: list[TemperatureUpdateError]
