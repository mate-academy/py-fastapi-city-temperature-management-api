from typing import Annotated

from pydantic import BaseModel, Field, ConfigDict


class CityBase(BaseModel):
    name: Annotated[str, Field(max_length=100)]
    additional_info: str


class CityCreate(CityBase):
    pass


class CityUpdate(CityBase):
    name: Annotated[str, Field(max_length=100)] | None = None
    additional_info: str | None = None


class CityRead(CityBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
