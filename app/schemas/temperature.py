from datetime import datetime

from pydantic import BaseModel
from pydantic import ConfigDict


class TemperatureResponse(BaseModel):
    id: int
    city_id: int
    date_time: datetime
    temperature: float

    model_config = ConfigDict(from_attributes=True)
