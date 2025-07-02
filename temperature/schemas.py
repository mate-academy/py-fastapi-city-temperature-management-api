from datetime import datetime

from pydantic import BaseModel


class TemperatureBase(BaseModel):
    city_id: int
    temperature: float


class TemperatureUpdate(BaseModel):
    cities_total: int
    updated: int
    missing: list[str]


class TemperatureResponse(TemperatureBase):
    id: int
    date_time: datetime

    model_config = {"from_attributes": True}
