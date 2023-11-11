from datetime import datetime

from pydantic import BaseModel


class TemperatureBase(BaseModel):
    date_time: datetime
    temperature: float

    class Config:
        from_attributes = True


class TemperatureRead(TemperatureBase):
    id: int
    city_id: int


class TemperatureCreateUpdate(TemperatureBase):
    city_id: int
