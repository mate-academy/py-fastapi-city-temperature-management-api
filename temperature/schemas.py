from datetime import datetime

from pydantic import BaseModel


class TemperatureBase(BaseModel):
    datetime: datetime
    temperature: float


class TemperatureCreate(TemperatureBase):
    city_id: int


class Temperature(TemperatureBase):
    id: int
    city_id: int

    model_config = {
        "from_attributes": True
    }
