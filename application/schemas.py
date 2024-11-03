from datetime import datetime

from pydantic import BaseModel


class CityBase(BaseModel):
    name: str
    additional_info: str = None


class CityCreate(CityBase):
    pass


class CityInfo(CityBase):
    id: int

    class Config:
        from_attributes = True


class TemperatureBase(BaseModel):
    temperature: int


class TemperatureCreate(TemperatureBase):
    city_id: int


class TemperatureInfo(TemperatureBase):
    id: int
    date_time: datetime
    city: CityInfo

    class Config:
        from_attributes = True
