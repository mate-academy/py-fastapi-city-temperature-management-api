from datetime import datetime
from pydantic import BaseModel


class TemperatureBaseSerializer(BaseModel):
    city_id: int
    date_time: datetime
    temperature: float


class TemperatureCreateSerializer(TemperatureBaseSerializer):
    pass


class TemperatureUpdateSerializer(BaseModel):
    message: str


class TemperatureSerializer(TemperatureBaseSerializer):
    id: int

    class Config:
        from_attributes = True
