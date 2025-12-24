from pydantic import BaseModel
from datetime import datetime
from cities.schemas import CityOut


class TemperatureOut(BaseModel):
    id: int
    temperature: float
    date_time: datetime
    city: CityOut

    class Config:
        from_attributes = True
