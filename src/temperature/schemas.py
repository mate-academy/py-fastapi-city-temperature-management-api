from datetime import datetime

from pydantic import BaseModel, Field


class TemperatureData(BaseModel):
    temperature: float = Field(...)

class TemperatureRead(BaseModel):
    id: int
    city_id: int
    date_time: datetime
    temperature: float

    model_config = {
        "from_attributes": True
    }
