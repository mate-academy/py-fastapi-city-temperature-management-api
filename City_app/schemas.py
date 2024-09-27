from typing import List, Optional

from pydantic import BaseModel, Field

from Temperature_app.schemas import Temperature


class CityBase(BaseModel):
    name: str = Field(max_length=176)
    additional_info: str


class CityCreate(CityBase):
    pass


class City(CityBase):
    id: int
    temperatures: Optional[List[Temperature]] = []

    class Config:
        from_attributes = True
