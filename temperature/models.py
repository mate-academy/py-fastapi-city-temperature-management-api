from datetime import datetime

from pydantic import BaseModel


class TemperatureModel(BaseModel):
    id: int
    city_id: int
    date_time: datetime
    temperature: float
