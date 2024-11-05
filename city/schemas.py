from pydantic import BaseModel
from typing import Optional


class CityBase(BaseModel):
    name: str
    additional_info: Optional[str] = None


class CityCreate(CityBase):
    pass


class CityRead(CityBase):
    id: int
    name: str


CityRead.update_forward_refs()
