from typing import Optional, List

from pydantic import BaseModel


class City(BaseModel):
    name: str
    additional_info: str


class CityCreate(City):
    pass


class CityResponse(City):
    id: int

    class Config:
        from_attributes = True


class CityUpdate(BaseModel):
    name: Optional[str] = None
    additional_info: Optional[str] = None
