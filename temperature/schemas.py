from datetime import datetime
from pydantic import BaseModel


class TemperatureRead(BaseModel):
    id: int
    city_id: int
    date_time: datetime
    temperature: float


    class Config:
        from_attributes = True