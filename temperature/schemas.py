from datetime import datetime

from pydantic import BaseModel, ConfigDict


class TemperatureBase(BaseModel):
    temperature: float
    city_id: int
    date_time: datetime

class Temperature(TemperatureBase):
    model_config = ConfigDict(from_attributes=True)

    id: int

class TemperatureUpdate(TemperatureBase):
    temperature: float
    city_id: int
    date_time: datetime | None = None
