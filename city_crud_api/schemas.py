from pydantic import BaseModel
from typing import Optional


class CityBase(BaseModel):
    name: str
    additional_info: Optional[str] = None

    class Config:
        orm_mode = True


class CityCreate(CityBase):
    pass


class City(CityBase):
    id: int


class CityUpdate(BaseModel):
    name: Optional[str] = None
    additional_info: Optional[str] = None

    class Config:
        orm_mode = True
