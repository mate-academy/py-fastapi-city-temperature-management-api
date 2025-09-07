from datetime import datetime
from typing import Optional

from pydantic import BaseModel

class TemperatureBaseSchema(BaseModel):
    city_id: int
    date_time: datetime
    temperature: float


class TemperatureCreateSchema(TemperatureBaseSchema):
    pass


class TemperatureUpdateSchema(TemperatureBaseSchema):
    pass


class TemperaturePartialUpdateSchema(TemperatureBaseSchema):
    date_time: Optional[datetime] = None
    temperature: Optional[float] = None


class TemperatureReadSchema(TemperatureBaseSchema):
    id: int

    class Config:
        from_attributes = True
