import datetime
from typing import Optional

from pydantic import BaseModel

from city.schemas import ListCity


class ListWeather(BaseModel):
    id: int
    city_id: int
    date_time: datetime.datetime
    temperature: float
    city: ListCity


class UpdateWeather(BaseModel):
    response_line: str
