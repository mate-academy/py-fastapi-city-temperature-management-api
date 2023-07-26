from pydantic import BaseModel
from datetime import datetime

class TemperatureBase(BaseModel):
    date_time: datetime
    temperature: float

class TemperatureCreate(TemperatureBase):
    city_id: int

class Temperature(TemperatureBase):
    id: int
    city_id: int

    class Config:
        orm_mode = True
