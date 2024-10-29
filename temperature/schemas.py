from pydantic import BaseModel
from datetime import datetime


class TemperatureBase(BaseModel):
    date_time: datetime
    temperature: float


class Temperature(TemperatureBase):
    id: int

    class Config:
        orm_mode = True
