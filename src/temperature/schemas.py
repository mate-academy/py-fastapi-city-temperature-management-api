from datetime import datetime

from pydantic import ConfigDict, BaseModel

from src.city import schemas


class CityTemperatureBase(BaseModel):
    date_time: datetime
    temperature: int


class CityTemperatureCreate(CityTemperatureBase):
    city_id: int


class CityTemperature(CityTemperatureBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    city: schemas.City
