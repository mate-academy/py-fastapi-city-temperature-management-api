from datetime import datetime

from pydantic import BaseModel


class TemperatureBase(BaseModel):
    date_time: datetime
    temperature: float


class Temperature(TemperatureBase):
    id: int
    city_id: int

    class Config:
        from_attributes = True


class TemperatureUpdate(BaseModel):
    message: str
    invalid_cities: str
