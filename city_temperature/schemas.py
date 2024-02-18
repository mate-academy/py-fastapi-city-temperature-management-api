from datetime import datetime

from pydantic import BaseModel


class TemperatureBase(BaseModel):
    city_id: int
    date_time: datetime
    temperature: float


class TemperatureCreateUpdate(BaseModel):
    temperature: float
    city_id: int


class TemperatureRead(TemperatureBase):
    id: int

    class Config:
        from_attributes = True


class CityBase(BaseModel):
    name: str
    additional_info: str | None = None


class CityCreateUpdate(CityBase):
    pass


class CityRead(CityBase):
    id: int
    temperatures: list[TemperatureRead] = []

    class Config:
        from_attributes = True
