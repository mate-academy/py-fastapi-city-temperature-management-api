from typing import List

from pydantic import BaseModel


class CityCreateSchema(BaseModel):
    name: str
    additional_info: str | None = None


class CityResponseSchema(CityCreateSchema):
    id: int

    model_config = {"from_attributes": True}


class CityListSchema(BaseModel):
    cities: List["CityResponseSchema"]
