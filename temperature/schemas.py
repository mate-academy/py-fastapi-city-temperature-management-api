from datetime import datetime

from pydantic import BaseModel


class TemperatureSchema(BaseModel):
    city_id: int
    date_time: datetime
    temperature: float


class TemperatureListSchema(TemperatureSchema):
    id: int
