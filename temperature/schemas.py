from pydantic import BaseModel
from datetime import datetime


class TemperatureBase(BaseModel):
    city_id: int
    date_time: datetime = datetime.now()
    temperature: float


class TemperatureCreate(TemperatureBase):
    pass


class Temperature(TemperatureBase):
    id: int

    class Config:
        from_attributes = True
