from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class CityBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    additional_info: str | None = Field(default=None, max_length=500)


class CityCreate(CityBase):
    pass


class CityUpdate(CityBase):
    pass


class City(CityBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class Temperature(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    city_id: int
    date_time: datetime
    temperature: float


class TemperatureUpdateResult(BaseModel):
    created: list[Temperature]
    errors: dict[int, str]
