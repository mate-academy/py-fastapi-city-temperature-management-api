import datetime

from fastapi.openapi.models import Schema


class TemperatureBase(Schema):
    city_id: int
    date_time: datetime.datetime
    temperature: float


class TemperatureList(TemperatureBase):
    id: int

    class Config:
        from_attributes = True
