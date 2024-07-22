import datetime
from pydantic import BaseModel


class TemperatureBase(BaseModel):
    id: int
    city_id: int
    date_time: datetime.datetime
    temperature: float
class TemperatureCreate(TemperatureBase):
    pass
class Temperature(TemperatureBase):
    id: int

    class Config:
        orm_mode = True