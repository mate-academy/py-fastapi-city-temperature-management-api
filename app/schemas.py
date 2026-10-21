from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class CityBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    additional_info: str | None = None


class CityCreate(CityBase):
    pass


class CityUpdate(CityBase):
    pass


class City(CityBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class Temperature(BaseModel):
    id: int
    city_id: int
    date_time: datetime
    temperature: float

    model_config = ConfigDict(from_attributes=True)
