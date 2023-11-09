from datetime import datetime

from pydantic import BaseModel


class CityBase(BaseModel):
    name: str
    additional_info: str


class CityList(CityBase):
    id: int

    class Config:
        orm_mode = True


class TemperatureBase(BaseModel):
    city_id: int
    city_id: datetime
    temperature: float


class TemperatureList(CityBase):
    id: int

    class Config:
        orm_mode = True
