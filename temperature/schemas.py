from datetime import datetime
from pydantic import BaseModel
from city.schemas import City


class TemperatureBase(BaseModel):
    temperature: float


class TemperatureCreate(TemperatureBase):
    city_id: int


class TemperatureWithCity(TemperatureBase):
    id: int
    city_id: int
    recorded_at: datetime
    city: City

    class Config:
        orm_mode = True


class Temperature(TemperatureBase):
    id: int
    city_id: int
    recorded_at: datetime

    class Config:
        orm_mode = True
