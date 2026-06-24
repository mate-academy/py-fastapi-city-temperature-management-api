from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class CityCreate(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    additional_info: str | None = Field(default=None, max_length=500)


class City(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    additional_info: str | None


class Temperature(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    city_id: int
    date_time: datetime
    temperature: float
