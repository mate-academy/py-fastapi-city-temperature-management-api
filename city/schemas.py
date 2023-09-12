from pydantic import BaseModel
from typing import Optional


class CityBase(BaseModel):
    name: str
    additional_info: Optional[str] = None


class CityBaseCreate(CityBase):
    pass


class City(CityBase):
    id: int

    class Config:
        orm_mode = True
