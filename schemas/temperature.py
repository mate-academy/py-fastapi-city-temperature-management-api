from pydantic import BaseModel, constr
from datetime import datetime


class TemperatureCreateSchema(BaseModel):
    city_id: int
    date_time: datetime
    temperature: float


class TemperatureReadSchema(BaseModel):
    id: int
    city_id: int
    date_time: datetime
    temperature: float

    class Config:
        from_attributes = True
