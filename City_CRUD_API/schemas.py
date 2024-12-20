from typing import Optional

from pydantic import BaseModel


class CityBase(BaseModel):
    name: str
    additional_info: str


class CityCreate(CityBase):
    pass


class CityList(CityBase):
    id: int

    class Config:
        # from_attributes = True
        orm_mode = True


class CityDelete(CityBase):
    id: int

    class Config:
        # from_attributes = True
        orm_mode = True


class CityUpdate(CityBase):
    id: int
    name: Optional[str] = None
    additional_info: Optional[str] = None

    class Config:
        # from_attributes = True
        orm_mode = True
