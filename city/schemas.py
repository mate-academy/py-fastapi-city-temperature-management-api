from datetime import datetime

from pydantic import BaseModel


class CityBase(BaseModel):
    name: str


class City(CityBase):
    id: int
    additional_info: str


class CityCreate(CityBase):
    additional_info: str


class Temperature(BaseModel):
    id: int
    temperature: float
    city_id: int
    date_time: datetime

    class Config:
        from_attributes = True
