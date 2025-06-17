from datetime import datetime

from pydantic import BaseModel


class TemperatureSchema(BaseModel):
    city_id: int
    date_time: datetime
    temperature: float


class TemperatureCreateSchema(TemperatureSchema):
    pass


class TemperatureReadSchema(TemperatureSchema):
    id: int

    class Config:
        from_attributes = True
