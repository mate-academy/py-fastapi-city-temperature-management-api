from datetime import datetime

from pydantic import BaseModel


class City(BaseModel):
    id: int
    name: str
    additional_info: str | None = None


class Temperature(BaseModel):
    id: int
    city_id: int
    date_time: datetime
    temperature: float
