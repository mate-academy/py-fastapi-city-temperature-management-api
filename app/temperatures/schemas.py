from datetime import datetime
from pydantic import BaseModel, ConfigDict


class TemperatureResponse(BaseModel):
    id: int
    city_id: int
    temperature: float
    date_time: datetime

    model_config = ConfigDict(from_attributes=True)
