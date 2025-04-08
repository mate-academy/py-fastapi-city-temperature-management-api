from pydantic import BaseModel
from datetime import datetime

class TemperatureBase(BaseModel):
    city_id: int
    temperature: float
    date_time: datetime

class TemperatureOut(TemperatureBase):
    id: int

    class Config:
        orm_mode = True
