from pydantic import BaseModel
from datetime import datetime
from typing import List, Optional


class CityBase(BaseModel):
    name: str
    additional_info: Optional[str] = None


class CityCreate(CityBase):
    pass


class City(CityBase):
    id: int  # noqa:VNE003
    temperatures: List['Temperature'] = []

    class Config:
        from_attributes = True


class TemperatureBase(BaseModel):
    date_time: datetime
    temperature: float


class TemperatureCreate(TemperatureBase):
    pass


class Temperature(TemperatureBase):
    id: int  # noqa:VNE003
    city_id: int

    class Config:
        from_attributes = True


City.update_forward_refs()
