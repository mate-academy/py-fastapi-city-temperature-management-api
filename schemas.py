from pydantic import BaseModel
import datetime


class CityCreate(BaseModel):
    name: str
    additional_info: str


class CityResponse(CityCreate):
    id: int

    class Config:
        from_attributes = True


class TemperatureResponse(BaseModel):
    id: int
    city_id: int
    date_time: datetime.datetime
    temperature: float

    class Config:
        from_attributes = True
