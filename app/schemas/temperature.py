from datetime import datetime

from pydantic import BaseModel, ConfigDict


class Temperature(BaseModel):
    date_time: datetime
    temperature: float


class TemperatureCreate(Temperature):
    pass


class TemperatureRead(Temperature):
    id: int
    city_id: int
    model_config = ConfigDict(from_attributes=True)
