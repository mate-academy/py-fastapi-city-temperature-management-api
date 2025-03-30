from pydantic import BaseModel
from typing import List, Optional


class CreateCityRequestSchema(BaseModel):
    name: str
    additional_info: str


class CreateCityResponseSchema(BaseModel):
    id: int
    name: str
    additional_info:str


class ListCitiesResponseSchema(BaseModel):
    cities: List[CreateCityResponseSchema]
    prev_page: Optional[str] = None
    next_page: Optional[str] = None
    total_pages: int
    total_cities: int


class CityDetailResponseSchema(CreateCityResponseSchema):
    pass


class CityChangeRequestSchema(BaseModel):
    name: Optional[str] = None
    additional_info: Optional[str] = None


class CityNameSchema(BaseModel):
    name: str
