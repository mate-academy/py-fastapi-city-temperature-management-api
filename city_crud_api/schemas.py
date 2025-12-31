from pydantic import BaseModel, Field, ConfigDict

import temperature_api.schemas
from temperature_api.models import DBTemperature


class CityBaseModel(BaseModel):
    name: str = Field(max_length=64)
    additional_info: str | None = Field(max_length=255)


class CityCreate(CityBaseModel):
    pass


class CityUpdate(CityBaseModel):
    pass


class City(CityBaseModel):
    model_config = ConfigDict(from_attributes=True)
    id: int

