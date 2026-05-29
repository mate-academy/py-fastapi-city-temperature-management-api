from datetime import date

from pydantic import BaseModel, ConfigDict


class CityBase(BaseModel):
    name: str
    additional_info: str


class CityCreate(CityBase):
    pass


class CityList(CityBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class CityUpdate(CityBase):
    pass


class TemperatureBase(BaseModel):
    city_id: int
    date_time: date
    temperature: float


class TemperatureCreate(TemperatureBase):
    pass


class TemperatureList(TemperatureBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class TemperatureUpdate(TemperatureBase):
    pass
