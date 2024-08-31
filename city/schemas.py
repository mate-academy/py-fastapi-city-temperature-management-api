from typing import Optional

from pydantic import BaseModel


class CityBase(BaseModel):
    name: str
    additional_info: Optional[str] = None


class CityIn(CityBase):
    ...


class City(CityBase):
    id: int


class CityPatch(CityIn):
    name: Optional[str] = None
    additional_info: Optional[str] = None
