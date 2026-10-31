from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class CityCreate(BaseModel):
    name: str = Field(min_length=1, max_length=200, pattern=r".*\S.*")
    additional_info: str | None = None


class CityRead(CityCreate):
    model_config = ConfigDict(from_attributes=True)
    id: int


class TemperatureRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int
    city_id: int
    date_time: datetime
    temperature: float
