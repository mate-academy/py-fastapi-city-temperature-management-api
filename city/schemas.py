import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class CityName(BaseModel):
    id: int
    name: str
    model_config = ConfigDict(from_attributes=True)


class CityBase(BaseModel):
    name: str
    additional_info: Optional[str] = None


class CityCreate(CityBase):
    pass


class CityUpdate(CityBase):
    name: Optional[str] = None
    additional_info: Optional[str] = None


class CityList(CityBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class TemperatureBase(BaseModel):
    city_id: int
    temperature: float


class TemperatureCreate(TemperatureBase):
    date_time: datetime.datetime | None = None


class TemperatureList(TemperatureBase):
    id: int
    date_time: datetime.datetime
    city: CityName
    model_config = ConfigDict(from_attributes=True)
