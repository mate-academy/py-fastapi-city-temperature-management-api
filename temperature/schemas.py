from pydantic import BaseModel
from datetime import datetime


class TemperatureBase(BaseModel):
    city_id: int
    date_time: datetime
    temp_c: float
    temp_f: float


class CreateTemperature(TemperatureBase):
    pass


class UpdateTemperature(TemperatureBase):
    id: int


class Temperature(TemperatureBase):
    id: int

    class Config:
        from_attributes = True
