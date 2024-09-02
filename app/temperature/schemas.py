from datetime import datetime

from pydantic import BaseModel


class TemperatureBase(BaseModel):
    city_id: int
    date_time: datetime
    temperature: float


class TemperatureUpdate(TemperatureBase):
    pass


class TemperatureRead(TemperatureBase):
    id: int

    class Config:
        from_attributes = True
