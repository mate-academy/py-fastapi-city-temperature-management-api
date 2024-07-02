from datetime import datetime

from pydantic import BaseModel


class TemperatureBase(BaseModel):
    city_id: str
    date_time: datetime
    temperature: float


class TemperatureCreate(TemperatureBase):
    pass


class Temperature(TemperatureBase):
    id: str

    class Config:
        orm_mode = True
