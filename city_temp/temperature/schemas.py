from pydantic import BaseModel
import datetime


class TemperatureBase(BaseModel):
    city_id: int
    datetime: datetime.datetime
    temperature: float

    class Config:
        from_attributes = True
        orm_mode = True


class TemperatureCreate(TemperatureBase):
    pass


class Temperature(TemperatureBase):
    id: int
