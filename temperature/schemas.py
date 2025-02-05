from datetime import datetime

from pydantic import BaseModel


class TemperatureBase(BaseModel):
    city_id: int
    date_time: datetime
    temperature: float


class TemperatureCreate(TemperatureBase):
    pass


class TemperatureUpdate(TemperatureBase):
    pass


class TemperatureDelete(TemperatureBase):
    pass


class TemperatureResponse(TemperatureBase):
    id: int

    class Config:
        from_attributes = True
