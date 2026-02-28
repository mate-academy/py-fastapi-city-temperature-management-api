import datetime

from pydantic import BaseModel, ConfigDict


class CityBase(BaseModel):
    name: str
    additional_info: str

class CityCreate(CityBase):
    pass

class City(CityBase):
    model_config = ConfigDict(from_attributes=True)

    id: int

class TemperatureBase(BaseModel):
    temperature: float

class TemperatureCreate(TemperatureBase):
    city_id: int

class Temperature(TemperatureBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    city_id: int
    date_time: datetime.datetime