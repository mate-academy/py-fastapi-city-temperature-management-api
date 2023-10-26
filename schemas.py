from pydantic import BaseModel
from datetime import datetime


class CityBase(BaseModel):
    name: str
    additional_info: str = None


class CityCreate(CityBase):
    pass


class CityList(CityBase):
    id: int

    class Config:
        orm_mode = True


class TemperatureBase(BaseModel):
    city_id: int
    date_time: datetime
    temperature: float


class TemperatureCreate(TemperatureBase):
    pass


class TemperatureList(TemperatureBase):
    id: int

    class Config:
        orm_mode = True
