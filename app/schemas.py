from datetime import datetime
from typing import Optional
from pydantic import BaseModel, ConfigDict


class CityBase(BaseModel):
    name: str
    additional_info: Optional[str] | None = None


class CityCreate(CityBase):
    pass


class CityList(CityBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class CityUpdate(CityBase):
    pass


class TemperatureBase(BaseModel):
    date_time: datetime
    temperature: float


class TemperatureCreate(TemperatureBase):
    city_id: int


class TemperatureList(TemperatureBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    city_id: int
