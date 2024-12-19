from pydantic import BaseModel
from datetime import datetime


class OnlineResponse(BaseModel):
    status: str
    message: str


class TemperatureBase(BaseModel):
    city_id: int
    date_time: datetime
    temperature: float

class TemperatureCreate(TemperatureBase):
    pass

class Temperature(TemperatureBase):
    id: int

    class Config:
        orm_mode = True
