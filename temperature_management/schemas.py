from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CityBase(BaseModel):
    name: str
    additional_info: str


class CityCreate(CityBase):
    pass


class City(CityBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class CityUpdate(CityBase):
    pass


class CityPartialUpdate(BaseModel):
    name: str | None = None
    additional_info: str | None = None


class CityTemperature(BaseModel):
    name: str


class TemperatureBase(BaseModel):
    city: CityTemperature
    date_time: datetime
    temperature: float


class Temperature(TemperatureBase):
    model_config = ConfigDict(from_attributes=True)
    id: int


class TemperatureForCity(BaseModel):
    id: int
    date_time: datetime
    temperature: float


class CityWithTemperatures(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    city: str
    temperatures: list[TemperatureForCity]
