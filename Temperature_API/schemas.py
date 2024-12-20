from datetime import datetime

from pydantic import BaseModel


class TemperatureBase(BaseModel):
    date_time: datetime
    temperature: float


class TemperatureCreate(TemperatureBase):
    pass


class TemperatureList(TemperatureBase):
    id: int

    class Config:
        # from_attributes = True
        orm_mode = True
