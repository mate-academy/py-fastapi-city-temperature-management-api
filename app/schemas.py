from pydantic import BaseModel, ConfigDict

import datetime


class CityBase(BaseModel):
    name: str
    additional_info: str | None = None


class CityCreate(CityBase):
    pass


class CityUpdate(CityBase):
    pass


class CityRead(CityBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class TemperatureBase(BaseModel):
    city_id: int
    date_time: datetime.datetime
    temperature: float


class TemperatureRead(TemperatureBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
