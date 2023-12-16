from typing import Literal

from pydantic import BaseModel, ConfigDict, Field


class CityBase(BaseModel):
    name: str = Field(min_length=2)
    additional_info: str | None = None


class CityCreate(CityBase):
    pass


class City(CityBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class CRUDDetails(BaseModel):
    id: int | None
    message: str = ""
    status: Literal["success", "does_not_exists", "failure"]
