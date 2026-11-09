from pydantic import BaseModel, ConfigDict
import datetime


class CityBase(BaseModel):
    name: str
    additional_info: str
    latitude: float
    longitude: float


class CityCreate(CityBase):
    pass


class CityResponse(CityBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class TemperatureBase(BaseModel):
    date_time: datetime.datetime
    temperature: float
    city_id: int


class TemperatureCreate(TemperatureBase):
    pass


class TemperatureResponse(TemperatureBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
