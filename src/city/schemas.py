from typing import Optional

from pydantic import BaseModel


class CityIn(BaseModel):
    name: str
    additional_info: Optional[str] = None


class City(BaseModel):
    id: int
    name: str


class CityDetailed(BaseModel):
    id: int
    name: str
    additional_info: Optional[str] = None
