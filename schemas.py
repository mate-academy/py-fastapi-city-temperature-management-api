from pydantic import BaseModel, ConfigDict
import datetime


class CityBase(BaseModel):
    name: str
    additional_info: str | None


class CityCreate(CityBase):
    pass


class City(CityBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class TemperatureBase(BaseModel):
    temperature: float
    date_time: datetime
    city_id: int


class TemperatureCreate(TemperatureBase):
    pass


class Temperature(TemperatureBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
