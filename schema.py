from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CityBase(BaseModel):
    name: str
    additional_info: str


class CityCreate(CityBase):
    ...


class CityReadBase(CityBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class CityRead(CityReadBase):
    ...


class TemperatureRead(BaseModel):
    id: int
    city_id: int
    temperature: float
    date_time: datetime
    model_config = ConfigDict(from_attributes=True)