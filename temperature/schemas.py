from datetime import datetime

from pydantic import BaseModel


class TemperatureBase(BaseModel):
    city_id: int
    temperature: float


class TemperatureCreate(TemperatureBase):
    pass


class TemperatureResponse(TemperatureBase):
    id: int
    date_time: datetime

    class Config:
        orm_mode = True
