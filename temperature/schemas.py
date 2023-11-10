from datetime import datetime

from pydantic import BaseModel


class TemperatureBase(BaseModel):
    city_id: int
    date_time: datetime
    temperature: float


class TemperatureList(TemperatureBase):
    id: int

    class Config:
        orm_mode = True
