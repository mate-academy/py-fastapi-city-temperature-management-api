from datetime import datetime
from typing import Optional

from pydantic import BaseModel

from app.schemes.city import CityResponse


class Temperature(BaseModel):
    city_id: int
    date_time: datetime
    temperature: float


class TemperatureCreate(Temperature):
    pass


class TemperatureResponse(Temperature):
    id: int
    city: CityResponse

    class Config:
        from_attributes = True


class TemperatureUpdate(BaseModel):
    city_id: Optional[int] = None
    date_time: Optional[datetime] = None
    temperature: Optional[float] = None
