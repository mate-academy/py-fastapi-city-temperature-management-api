from datetime import datetime

from pydantic import BaseModel


class TemperatureIn(BaseModel):
    city_id: int
    temperature: float


class Temperature(TemperatureIn):
    id: int
    city_id: int
    date_time: datetime
    temperature: float

    class Config:
        orm_mode = True
