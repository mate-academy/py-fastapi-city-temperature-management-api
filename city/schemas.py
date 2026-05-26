from pydantic import BaseModel

from typing import Optional


class CityBase(BaseModel):
    name: str
    additional_info: Optional[str] = None


class CityCreate(CityBase):
    pass


class CityResponse(CityBase):
    id: int

    class Config:
        orm_mode = True


class CityUpdate(CityBase):
    name: Optional[str] = None
    additional_info: Optional[str] = None
