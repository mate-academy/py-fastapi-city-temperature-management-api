from pydantic import BaseModel
from datetime import datetime

class TemperatureBase(BaseModel):
    temperature: float

class TemperatureCreate(TemperatureBase):
    city_id: int

class TemperatureOut(TemperatureBase):
    id: int
    city_id: int
    date_time: datetime

    class Config:
        from_attributes = True
