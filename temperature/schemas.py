from datetime import datetime

from pydantic import BaseModel

from city import schemas


class TemperatureBase(BaseModel):

    date_time: datetime
    temperature: float


class TemperatureCreate(TemperatureBase):
    city_id: int


class TemperatureRead(TemperatureBase):
    id: int
    city: schemas.CityRead

    class Config:
        orm_mode = True


class TemperatureFailed(BaseModel):
    city: str
    status_code: int


class TemperatureSucceeded(BaseModel):
    city: str
    temperature: float
    date_time: datetime


class TemperatureUpdate(BaseModel):
    succeeded: list[TemperatureSucceeded]
    failed: list[TemperatureFailed]
