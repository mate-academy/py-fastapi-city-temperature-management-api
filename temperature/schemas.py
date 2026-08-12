from datetime import datetime

from pydantic import BaseModel, ConfigDict


class TemperatureCreate(BaseModel):
    date_time: datetime
    temperature: float
    city_id: int


class Temperature(BaseModel):
    id: int
    date_time: datetime
    temperature: float
    city_id: int
    model_config = ConfigDict(from_attributes=True)
