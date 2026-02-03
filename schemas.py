from datetime import datetime

from pydantic import BaseModel


class CityBase(BaseModel):
    name: str
    additional_info: str


class CityCreate(CityBase):
    pass


class City(CityBase):
    id: int

    class Config:
        from_attributes = True


class TemperatureRead(BaseModel):
    id: int
    city_id: int
    date_time: datetime
    temperature: float

    class Config:
        from_attributes = True
