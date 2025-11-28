from datetime import datetime

from pydantic import BaseModel


class City(BaseModel):
    name: str
    additional_info: str


class CityBaseCreate(City):
    pass


class CityBase(City):
    id: int

    model_config = {
        "from_attribute": True
    }


class CityUpdate(City):
    pass


class Temperature(BaseModel):
    city_id: int
    date_time: datetime
    temperature: float


class TemperatureCreate(Temperature):
    pass


class TemperatureBase(Temperature):
    id: int

    model_config = {
        "from_attribute": True
    }
