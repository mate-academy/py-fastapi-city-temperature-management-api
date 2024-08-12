from datetime import datetime

from pydantic import BaseModel

from city_app.schemas import CitySchema


class TemperatureBase(BaseModel):
    city_id: int
    date_time: datetime
    temperature: float


class TemperatureCreate(TemperatureBase):
    pass


class Temperature(TemperatureBase):
    id: int
    city: CitySchema

    class Config:
        from_attributes = True
