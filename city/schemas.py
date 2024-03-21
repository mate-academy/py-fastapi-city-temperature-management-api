from pydantic import BaseModel
from typing import Optional


class CityBase(BaseModel):
    name: str
    additional_info: Optional[str] = None


class CreateCity(CityBase):
    pass


class UpdateCity(BaseModel):
    name: Optional[str] = None
    additional_info: Optional[str] = None

    class Config:
        from_attributes = True


class City(CityBase):
    id: int

    class Config:
        from_attributes = True
