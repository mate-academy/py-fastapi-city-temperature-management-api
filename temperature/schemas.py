from pydantic import BaseModel
from datetime import datetime


class TemperatureBase(BaseModel):
    city_name: str
    date_time_utc: datetime
    temperature: str


class Temperature(TemperatureBase):
    id: int

    class Config:
        from_attributes = True
