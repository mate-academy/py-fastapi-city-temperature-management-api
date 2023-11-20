from datetime import datetime
from pydantic import BaseModel


class TemperatureBaseSerializer(BaseModel):
    city_id: int
    date_time: datetime
    temperature: float


class TemperatureSerializer(TemperatureBaseSerializer):
    id: int

    class Config:
        from_attributes = True
