from pydantic import BaseModel
from datetime import datetime


class TemperatureBase(BaseModel):
    pass


class CreateTemperatureRequest(TemperatureBase):
    city_id: int
    date_time: str
    temperature: float


class TemperatureResponse(TemperatureBase):
    id: int
    city_id: int
    date_time: str
    temperature: float

    class Config:
        from_attributes = True


class TemperatureUpdateResponse(BaseModel):
    message: str
    updated_cities: int
    temperatures_added: int
