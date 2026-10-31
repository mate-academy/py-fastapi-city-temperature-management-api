from datetime import datetime

from pydantic import BaseModel, ConfigDict


class Temperature(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    city_id: int
    date_time: datetime
    temperature: float
