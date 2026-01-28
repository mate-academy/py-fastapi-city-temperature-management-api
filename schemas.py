from datetime import datetime
from typing import Optional
from pydantic import BaseModel


class CityBase(BaseModel):
    name: str
    additional_info: Optional[str] = None


class CityCreate(CityBase):
    pass


class CityResponse(CityBase):
    id: int

    class Config:
        orm_mode = True


class TemperatureResponse(BaseModel):
    id: int
    city_id: int
    date_time: datetime
    temperature: float

    class Config:
        orm_mode = True
