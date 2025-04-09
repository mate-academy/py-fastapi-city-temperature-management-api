from datetime import datetime

from pydantic import BaseModel


class TemperatureCreateSchema(BaseModel):
    city_id: int
    date_time: datetime
    temperature: float

    class Config:
        from_attributes = True


class TemperatureUpdateSchema(TemperatureCreateSchema):
    id: int
