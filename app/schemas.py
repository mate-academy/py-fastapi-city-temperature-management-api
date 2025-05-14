from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CityBase(BaseModel):
    name: str
    additional_info: str


class CityCreate(CityBase):
    pass


class CityUpdate(CityBase):
    pass


class CityDelete(BaseModel):
    message: str


class City(CityBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class TemperatureBase(BaseModel):
    date_time: datetime
    temperature: float


class TemperatureCreate(TemperatureBase):
    city_id: int


class Temperature(TemperatureBase):
    id: int
    city: City

    model_config = ConfigDict(from_attributes=True)


class TemperatureUpdate(BaseModel):
    message: str
