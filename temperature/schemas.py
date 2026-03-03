from pydantic import BaseModel
from datetime import datetime
from typing import Optional


class TemperatureBaseSchema(BaseModel):
    id: int
    city_id: int
    temperature: float
    date_time: datetime

    class Config:
        from_attributes = True


class CityMaxTemperatureSchema(BaseModel):
    city_id: int
    city_name: str
    max_temperature: Optional[float] = None

    class Config:
        from_attributes = True
