from datetime import datetime

from pydantic import (
    ConfigDict,
    BaseModel,
    field_validator
)

from city.schemas import CityReadSchema


class TemperatureInCityReadSchema(BaseModel):
    id: int
    temperature: float
    date_time: datetime


class TemperatureReadSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    temperature: float
    city: CityReadSchema
    date_time: datetime

    @field_validator('temperature')
    @classmethod
    def round_temperature(cls, value):
        return round(value, 2)


class TemperatureCreateSchema(BaseModel):
    temperature: float
    city_id: int

    @field_validator('temperature')
    @classmethod
    def round_temperature(cls, value):
        return round(value, 2)
