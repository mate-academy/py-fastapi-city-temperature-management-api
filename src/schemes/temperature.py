from pydantic import BaseModel
from datetime import datetime
from typing import List

from schemes.city import CityNameSchema


class TemperatureDetailSchema(BaseModel):
    id: int
    city: CityNameSchema
    date_time: datetime
    temperature: float


class TemperatureListResponseSchema(BaseModel):
    temperatures: List[TemperatureDetailSchema]
