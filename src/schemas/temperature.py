from datetime import datetime

from pydantic import BaseModel

from src import schemas


class TemperatureBase(BaseModel):
    date_time: datetime
    temperature: int


class TemperatureCreate(TemperatureBase):
    city_id: int


class Temperature(TemperatureBase):
    id: int
    city: schemas.City

    class Config:
        from_attributes = True
