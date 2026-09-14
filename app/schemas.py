from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CityBase(BaseModel):
    name: str
    additional_info: str


class CityCreate(CityBase):
    pass


class CityList(CityBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class TemperatureBase(BaseModel):
    city_id: int
    date_time: datetime
    temperature: float


class TemperatureList(TemperatureBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
