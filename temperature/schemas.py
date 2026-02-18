from datetime import datetime

from pydantic import BaseModel, ConfigDict

from city.schemas import CityReadSchema


class TemperatureReadSchema(BaseModel):
    id: int
    date_time: datetime
    temperature: float
    city: CityReadSchema

    model_config = ConfigDict(from_attributes=True)
