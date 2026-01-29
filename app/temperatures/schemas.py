from datetime import datetime
from pydantic import BaseModel, ConfigDict


class TemperatureBase(BaseModel):
    temperature: float
    city_id: int

class TemperatureCreate(TemperatureBase):
    pass


class TemperatureRead(TemperatureBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    date_time: datetime
