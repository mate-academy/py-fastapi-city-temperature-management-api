from pydantic import BaseModel
from datetime import datetime

class BaseTemperature(BaseModel):
    date_time: datetime
    temperature: float


class CreateTemperature(BaseTemperature):
    city_id: int


class GetTemperature(BaseTemperature):
    id: int
    city_id: int

    class Config:
        from_attributes = True