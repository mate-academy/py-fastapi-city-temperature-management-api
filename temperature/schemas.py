from datetime import datetime

from pydantic import BaseModel

from city import schemas


class TemperatureBase(BaseModel):
    temperature: float


class TemperatureCreate(BaseModel):
    city_id: int


class Temperature(TemperatureBase):
    id: int
    city: schemas.City
    date_time: datetime

    class Config:
        from_attributes = True
