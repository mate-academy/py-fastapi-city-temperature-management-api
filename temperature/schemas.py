from datetime import datetime

from pydantic import BaseModel

class TemperatureBase(BaseModel):
    date_time: datetime
    city_id: int
    temperature: str


class TemperatureCreate(TemperatureBase):
    city_id: int
