from datetime import datetime

from pydantic import BaseModel, Field


class TemperatureRead(BaseModel):
    id: int
    city_id: int
    date_time: datetime
    temperature: float

    class Config:
        from_attributes = True


class TemperatureCreate(BaseModel):
    city_id: int
    temperature: float = Field(description="Temperature in Celsius")
    date_time: datetime | None = None
