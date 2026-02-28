from pydantic import BaseModel, ConfigDict
from datetime import datetime

from city.schemas import CityDto


class TemperatureCreateDto(BaseModel):
    city_id: int
    date_time: datetime
    temperature: float

    model_config = ConfigDict(from_attributes=True)


class TemperatureDto(BaseModel):
    id: int
    city: CityDto
    date_time: datetime
    temperature: float

    model_config = ConfigDict(from_attributes=True)
