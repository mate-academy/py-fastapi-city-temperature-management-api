from typing import Optional

from pydantic import BaseModel


class CityBase(BaseModel):
    name: str
    additional_info: Optional[str] = None


class CityCreate(CityBase):
    pass


class CityUpdate(CityBase):
    name: Optional[str] = None
    additional_info: Optional[str] = None


class City(CityBase):
    id: int

    class Config:
        orm_mode = True
