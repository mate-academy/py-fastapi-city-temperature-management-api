from typing import Optional

from pydantic import BaseModel, Field


class CityBase(BaseModel):
    name: str
    additional_info: str | None = None


class CityCreateUpdate(CityBase):
    pass


class City(CityBase):
    id: int

    class Config:
        orm_mode = True
