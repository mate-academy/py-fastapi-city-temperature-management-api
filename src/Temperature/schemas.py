from datetime import datetime
from pydantic import BaseModel, ConfigDict
from src.base_schemas import CityDetail


class TemperatureBase(BaseModel):
    temperature: float
    date_time: datetime


class TemperatureRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    temperature: float
    date_time: datetime
    city: CityDetail
