import datetime

from pydantic import BaseModel

from cities import schemas


class TemperatureBase(BaseModel):
    city_id: int
    date_time: datetime.datetime
    temperature: float


class Temperature(TemperatureBase):
    id: int
    city: schemas.CityName

    class Config:
        orm_mode = True


class TemperatureUpdate(BaseModel):
    message: str
