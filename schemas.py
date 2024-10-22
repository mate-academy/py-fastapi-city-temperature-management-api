from datetime import datetime

from pydantic import BaseModel


class CityList(BaseModel):
    id: int
    name: str
    additional_info: str


class CityCreate(BaseModel):
    name: str
    additional_info: str


class Temperature(BaseModel):
    id: int
    city_id: int
    date_time: datetime
    temperature: float
