from datetime import datetime
from pydantic import BaseModel


class TemperatureBase(BaseModel):
    city_id: int
    temperature: float


class Temperature(TemperatureBase):
    id: int
    date_time: datetime

    class Config:
        orm_mode = True


class UpdateResponse(BaseModel):
    message: str
