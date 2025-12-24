from typing import Optional

from pydantic import BaseModel


class CityCreateSchema(BaseModel):
    name: str
    additional_info: Optional[str] = None


class CityUpdateSchema(BaseModel):
    name: Optional[str] = None
    additional_info: Optional[str] = None


class CityListSchema(BaseModel):
    id: int
    name: str
    additional_info: Optional[str] = None

    class Config:
        from_attributes = True


class CityOut(BaseModel):
    id: int
    name: str
