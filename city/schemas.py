from pydantic import BaseModel
from typing import Optional


class CityBase(BaseModel):
    name: str
    additional_info: Optional[str] = None


class CityCreate(CityBase):
    pass


class CityUpdate(CityBase):
    pass


class City(CityBase):
    id: int

    class Config:
        orm_mode = True
