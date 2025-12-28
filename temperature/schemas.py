from datetime import datetime
from pydantic import BaseModel, ConfigDict


class TemperatureBase(BaseModel):
    city_id: int
    temperature: float
    date_time: datetime | None = None


class TemperatureCreate(TemperatureBase):
    pass


class TemperatureList(TemperatureBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
