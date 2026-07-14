from datetime import datetime
from decimal import Decimal
from typing import Optional
from zoneinfo import ZoneInfo

from pydantic import BaseModel


class TemperatureBaseSchema(BaseModel):
    temperature: Decimal
    date_time: Optional[datetime] = None
    time_zone: str
    city_id: int


class TemperatureSchema(TemperatureBaseSchema):
    id: int
