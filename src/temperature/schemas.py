from pydantic import BaseModel, ConfigDict
from datetime import datetime

class TemperatureBase(BaseModel):
    city_id: int
    temperature: float

class TemperatureCreate(TemperatureBase):
    pass

class TemperatureRead(TemperatureBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    date_time: datetime

