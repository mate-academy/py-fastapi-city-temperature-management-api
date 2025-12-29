from datetime import datetime
from pydantic import BaseModel, ConfigDict

from schemas.city import CityRead


class TemperatureBase(BaseModel):
    date_time: datetime
    temperature: int


class TemperatureCreate(TemperatureBase):
    city_id: int


class TemperatureRead(TemperatureBase):
    id: int
    city: CityRead

    model_config = ConfigDict(from_attributes=True)
