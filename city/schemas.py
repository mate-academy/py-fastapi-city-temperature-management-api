from pydantic import BaseModel
from typing import Optional


class CityBase(BaseModel):
    name: str
    additional_info: str


class CityCreate(CityBase):
    pass


class CityUpdate(BaseModel):
    name: Optional[str] = None
    additional_info: Optional[str] = None


class City(CityBase):
    id: int

    class Config:
        from_attributes = True
