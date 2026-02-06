from typing import TypeVar, Generic, List

from pydantic import BaseModel, ConfigDict


T = TypeVar("T")


class PaginatedResponse(BaseModel, Generic[T]):
    page: int
    size: int
    total: int
    results: List[T]


class CityBase(BaseModel):
    name: str
    additional_info: str


class CityCreate(CityBase):
    pass


class CityUpdate(CityBase):
    pass


class CityPatch(BaseModel):
    name: str | None = None
    additional_info: str | None = None


class CityDelete(CityBase):
    pass


class City(CityBase):
    id: int

    class Config:
        model_config = ConfigDict(from_attributes=True)
