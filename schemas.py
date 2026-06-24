from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional


class CityBase(BaseModel):
    name: str
    additional_info: Optional[str] = None


class CityCreate(CityBase):
    pass


class City(CityBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


class TemperatureBase(BaseModel):
    temperature: float


class Temperature(TemperatureBase):
    id: int
    city_id: int
    date_time: datetime
    model_config = ConfigDict(from_attributes=True)
