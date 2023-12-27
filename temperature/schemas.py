from datetime import datetime

from pydantic import BaseModel


class TemperatureBase(BaseModel):
    date_time: datetime | None = None
    temperature: float


class Temperature(TemperatureBase):
    id: int
    city_id: int

    class Config:
        orm_mode = True
