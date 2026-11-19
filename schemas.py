from datetime import datetime

from pydantic import BaseModel


class TemperatureBase(BaseModel):
    temperature: float


class TemperatureCreate(TemperatureBase):
    city_id: int
    date_time: datetime


class Temperature(TemperatureBase):
    id: int
    city_id: int
    date_time: datetime

    model_config = {"from_attributes": True}


class CityBase(BaseModel):
    name: str
    additional_info: str | None = None


class CityCreate(CityBase):
    pass


class City(CityBase):
    id: int

    model_config = {"from_attributes": True}
