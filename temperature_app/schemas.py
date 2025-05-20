from typing import Optional
from datetime import datetime

from pydantic import BaseModel


class CityBaseSchema(BaseModel):
    name: str
    additional_info: Optional[str] = None


class TemperatureBaseSchema(BaseModel):
    city_id: int
    temperature: float
    date_time: datetime
