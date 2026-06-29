from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CityBase(BaseModel):
    name: str
    additional_info: str


class City(CityBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class CityCreate(CityBase):
    name: str
    additional_info: str | None = None


class CityUpdate(CityBase):
    name: str
    additional_info: str | None = None


class TemperatureBase(BaseModel):
    city_id: int
    date_time: datetime
    temperature: float


class Temperature(TemperatureBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class TemperatureCreate(TemperatureBase):
    pass
