from typing import Optional

from pydantic import BaseModel


class CityBase(BaseModel):
    name: str
    additional_info: str


class CityPatch(BaseModel):
    name: Optional[str] = None
    additional_info: Optional[str] = None


class CityRead(CityBase):
    id: int
