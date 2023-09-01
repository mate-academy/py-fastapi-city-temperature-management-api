from datetime import datetime

from pydantic import BaseModel


class TemperatureBase(BaseModel):
    city_id: int
    date_time: datetime
    temperature: float


class Temperature(TemperatureBase):
    id: int

    class Config:
        from_attributes = True


class UpdateTemperature(TemperatureBase):
    pass
