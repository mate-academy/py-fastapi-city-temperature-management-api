from datetime import datetime

from pydantic import BaseModel

from city import schemas


class TemperatureBase(BaseModel):
    date_time: datetime
    temperature: float


class Temperature(TemperatureBase):
    id: int
    city_name: str

    class Config:
        orm_mode = True


class TemperatureCreate(TemperatureBase):
    city_id: int


class TemperatureRetrieve(TemperatureBase):
    id: int
    city: schemas.City
