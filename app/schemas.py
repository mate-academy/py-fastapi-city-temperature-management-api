from datetime import datetime

from pydantic import BaseModel


class CityBase(BaseModel):
    name: str
    additional_info: str | None = None


class CityCreate(CityBase):
    pass


class CityResponse(CityBase):
    id: int

    class Config:
        from_attributes = True


class TemperatureResponse(BaseModel):
    id: int
    city_id: int
    date_time: datetime
    temperature: float

    class Config:
        from_attributes = True
