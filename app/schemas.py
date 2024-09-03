from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CityBase(BaseModel):
    name: str
    additional_info: str | None = None

class CityCreate(CityBase):
    pass

class City(CityBase):
    id: int

    model_config = ConfigDict(from_orm=True)


class TemperatureBase(BaseModel):
    city_id: int
    temperature: float

class TemperatureCreate(TemperatureBase):
    pass

class Temperature(TemperatureBase):
    id: int
    date_time: datetime

    model_config = ConfigDict(from_orm=True)

