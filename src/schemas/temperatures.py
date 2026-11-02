from datetime import datetime

from pydantic import BaseModel, ConfigDict

from schemas.cities import City


class TemperatureBaseModel(BaseModel):
    date_time: datetime
    temperature: float


class TemperatureCreate(TemperatureBaseModel):
    city_id: int


class Temperature(TemperatureBaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    city: City
