from datetime import datetime

from pydantic import BaseModel

from city_app.schemas import City


class TemperatureBase(BaseModel):
    date_time: datetime
    temperature: float
    city_id: int


class TemperatureCreate(TemperatureBase):
    pass


class Temperature(TemperatureBase):
    id: int
    city: "City"

    class Config:
        from_attributes = True
