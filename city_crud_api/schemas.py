from datetime import datetime

from pydantic import BaseModel


class CityBase(BaseModel):
    name: str
    additional_info: str


class CityCreate(CityBase):
    pass


class CityList(CityBase):
    id: int

    model_config = {
        "from_attributes": True
    }


class TemperatureBase(BaseModel):
    city_id: int
    date_time: datetime
    temperature: float


class TemperatureCreate(TemperatureBase):
    pass


class TemperatureList(TemperatureBase):
    id: int

    model_config = {
        "from_attributes": True
    }
