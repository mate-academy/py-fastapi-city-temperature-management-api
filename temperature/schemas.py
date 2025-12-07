from datetime import datetime

from pydantic import BaseModel, ConfigDict

from city.schemas import City


class TemperatureBase(BaseModel):
    date_time: datetime
    temperature: float


class Temperature(TemperatureBase):
    id: int
    city: City
    model_config = ConfigDict(from_attributes=True)


class TemperatureCreate(TemperatureBase):
    city_id: int
