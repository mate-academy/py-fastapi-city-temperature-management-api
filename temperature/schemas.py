from datetime import datetime

from pydantic import BaseModel

from city import schemas


class TemperatureBase(BaseModel):
    date_time: datetime
    temperature: float


class TemperatureCreate(TemperatureBase):
    city_id: int


class Temperature(TemperatureBase):
    city: schemas.CityName

    class Config:
        from_attributes = True
