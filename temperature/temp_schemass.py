from pydantic import BaseModel

from datetime import datetime


class TemperatureBase(BaseModel):
    city_id: int
    date_time: datetime
    temperature: float = None


class Temperature(TemperatureBase):

    class Config:
        orm_mode = True
