from datetime import date

from pydantic import BaseModel, ConfigDict


class CityBase(BaseModel):
    name: str
    additional_information: str


class CityCreate(CityBase):
    pass


class CityList(CityBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class CityUpdate(CityBase):
    pass


class TemperatureBase(BaseModel):
    city: CityList
    date_time: date
    temperature: str


class TemperatureCreate(TemperatureBase):
    city_id: int


class TemperatureList(TemperatureBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class TemperatureUpdate(TemperatureBase):
    city_id: int


