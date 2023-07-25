from typing import Optional
from pydantic import BaseModel


class City(BaseModel):
    id: int
    name: str
    additional_info: str = None

    class Config:
        orm_mode = True


class CityCreate(BaseModel):
    name: str
    additional_info: Optional[str] = None

