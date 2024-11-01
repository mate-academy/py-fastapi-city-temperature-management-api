from pydantic import BaseModel

from cities.schemas import CitySchema

from datetime import datetime


class TemperatureBaseSchema(BaseModel):
    date_time: datetime
    temperature: float


class TemperatureSchema(TemperatureBaseSchema):
    id: int
    city: CitySchema

    class Config:
        orm_mode = True
