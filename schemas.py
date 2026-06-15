from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import List, Optional

class TemperatureBase(BaseModel):
    date_time: datetime
    temperature: float


class TemperatureCreate(TemperatureBase):
    city_id: int


class Temperature(TemperatureBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    city_id: int
    city: Optional['City'] = None


class CityBase(BaseModel):
    name: str
    additional_info: Optional[str] = None


class CityCreate(CityBase):
    pass


class City(CityBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    temperatures: List[Temperature] = []
