from datetime import datetime
from City.schemas import CityList
from pydantic import BaseModel


class TemperatureBase(BaseModel):
    date_time: datetime
    temperature: float


class TemperatureList(TemperatureBase):
    id: int
    city: CityList
