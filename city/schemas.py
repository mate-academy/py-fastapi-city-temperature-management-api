from typing import Optional

from pydantic import BaseModel, Field


class CityBase(BaseModel):
    name: str
    additional_info: str


class CityCreateSchema(CityBase):
    pass


class CityRetrieveSchema(CityBase):
    id: int

    class Config:
        from_attributes = True


class CityListSchema(BaseModel):
    cities: list[CityRetrieveSchema]
    total_items: int
    total_pages: int
    prev_page: Optional[str]
    next_page: Optional[str]

    class Config:
        from_attributes = True


class CityUpdateSchema(BaseModel):
    name: Optional[str] = Field(None, max_length=255)
    additional_info: Optional[str] = Field(None, max_length=511)
