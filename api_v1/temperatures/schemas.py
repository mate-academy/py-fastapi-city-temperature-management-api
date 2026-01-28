from datetime import datetime
from pydantic import BaseModel, ConfigDict
from api_v1.cities.schemas import City


class TemperatureBase(BaseModel):
    date_time: datetime
    temperature: float


class TemperatureCreate(TemperatureBase):
    pass


class Temperature(TemperatureBase):
    id: int
    city: City

    model_config = ConfigDict(from_attributes=True)


class TemperatureUpdateResult(BaseModel):
    updated: list[Temperature]
    failed: dict[str, str]
