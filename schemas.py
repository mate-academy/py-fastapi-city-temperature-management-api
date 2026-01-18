from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime


class TemperatureBase(BaseModel):
    temperature: float
    date_time: Optional[datetime] = None


class TemperatureCreate(TemperatureBase):
    city_id: int


class Temperature(TemperatureBase):
    id: int
    city_id: int
    date_time: datetime

    model_config = {"from_attributes": True}


class CityBase(BaseModel):
    name: str
    additional_info: Optional[str] = None


class CityCreate(CityBase):
    pass


class City(CityBase):
    id: int

    model_config = {"from_attributes": True}
