from datetime import datetime

from pydantic import BaseModel


class Temperature(BaseModel):
    id: int
    city_id: int
    date_time: datetime
    temperature: str

class TemperatureUpdate(BaseModel):
    city_id: int
    temperature: str
