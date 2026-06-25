from datetime import datetime
from pydantic import BaseModel


class TemperatureBaseSchema(BaseModel):
    city_id: int
    date_time: datetime
    temperature: float


class TemperatureCreateSchema(TemperatureBaseSchema):
    pass


class TemperatureSchema(TemperatureBaseSchema):
    id: int
