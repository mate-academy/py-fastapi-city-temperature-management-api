from datetime import date

from pydantic import BaseModel


class TemperatureBase(BaseModel):
    city_id: int
    date_time: date
    temperature: float


class TemperatureCreate(TemperatureBase):
    pass


class Temperature(TemperatureBase):
    id: int

    class Config:
        orm_mode = True


class TemperatureRecord(BaseModel):
    city_name: str
    temperature: float

    class Config:
        orm_mode = True
