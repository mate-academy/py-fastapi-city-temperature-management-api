from datetime import datetime
from pydantic import BaseModel

class TemperatureBase(BaseModel):
    temperature: float
    date_time: datetime

class CityDetail(BaseModel):
    id: int
    name: str
    additional_info: str
