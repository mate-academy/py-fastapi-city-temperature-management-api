import datetime

from pydantic import BaseModel, ConfigDict


class CityBase(BaseModel):
    name: str
    additional_info: str


class CityCreate(CityBase):
    pass


class CityRead(CityBase):
    id: int
    model_config = ConfigDict(from_attributes=True)  # name і additional_info вже є в CityBase


class CityPartialUpdate(BaseModel):
    name: str | None = None
    additional_info: str | None = None


class TemperatureRead(BaseModel):
    id: int
    city_id: int
    date_time: datetime.datetime
    temperature: float

    model_config = ConfigDict(from_attributes=True)
