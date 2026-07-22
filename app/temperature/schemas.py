from datetime import datetime

from pydantic import BaseModel


class TemperatureBaseModel(BaseModel):
    id: int
    city_id: int
    date_time: datetime
    temperature: str
