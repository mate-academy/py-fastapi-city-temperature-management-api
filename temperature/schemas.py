from datetime import datetime
from pydantic import BaseModel
from models import City


class TemperatureBase(BaseModel):
    city_id: int
    date_time: datetime
    temperature: float


class TemperatureCreate(TemperatureBase):
    pass


class TemperatureList(TemperatureBase):
    id: int
    city: City

    class Config:
        orm_mode = True
        arbitrary_types_allowed = True
