from typing import Optional

from pydantic import BaseModel


class CityBaseSchema(BaseModel):
    name: str
    additional_info: str


class CityCreateSchema(CityBaseSchema):
    pass


class CitySchema(CityBaseSchema):
    id: int

    class Config:
        orm_mode = True


class CityUpdateSchema(BaseModel):
    name: Optional[str] = None
    additional_info: Optional[str] = None

    class Config:
        orm_mode = True