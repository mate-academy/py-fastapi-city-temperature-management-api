from datetime import datetime

from pydantic import BaseModel, Field


class TemperatureBaseModel(BaseModel):
    id: int
    city_id: int
    date_time: datetime = Field(exclude=True, default=datetime.now())
    temperature: str
