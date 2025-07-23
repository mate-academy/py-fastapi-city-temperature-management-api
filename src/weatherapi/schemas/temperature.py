import datetime

from pydantic import BaseModel, Field


class TemperatureBase(BaseModel):
    temperature: float = Field()
    date_time: datetime.datetime | None = None


class TemperatureCreate(TemperatureBase):
    city_id: int


class TemperatureRead(TemperatureCreate):
    id: int

    class Config:
        from_attributes = True
