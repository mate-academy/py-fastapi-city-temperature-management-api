import datetime

from pydantic import BaseModel


class CityBase(BaseModel):
    name: str
    additional_info: str = ""


class CityCreate(CityBase):
    pass


class CityUpdate(BaseModel):
    name: str | None = None
    additional_info: str | None = None


class City(CityBase):
    id: int

    model_config = {"from_attributes": True}


class TemperatureBase(BaseModel):
    city_id: int
    date_time: datetime.datetime
    temperature: float


class Temperature(TemperatureBase):
    id: int

    model_config = {"from_attributes": True}

