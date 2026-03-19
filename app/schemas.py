from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class CityBase(BaseModel):
    name: str
    additional_info: Optional[str] = None


class CreateCity(CityBase):
    pass


class UpdateCity(BaseModel):
    name: Optional[str] = None
    additional_info: Optional[str] = None


class CityOut(CityBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class TemperatureBase(BaseModel):
    city_id: int
    date_time: datetime
    temperature: float


class TemperatureCreate(TemperatureBase):
    pass


class TemperatureOut(TemperatureBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
