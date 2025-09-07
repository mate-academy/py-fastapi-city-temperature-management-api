from pydantic import BaseModel

from typing import Optional


class CityBaseSchema(BaseModel):
    name: str
    additional_info: str


class CityCreateSchema(CityBaseSchema):
    pass


class CityUpdateSchema(CityBaseSchema):
    pass


class CityPartialUpdateSchema(CityBaseSchema):
    name: Optional[str] = None
    additional_info: Optional[str] = None


class CityReadSchema(CityBaseSchema):
    id: int

    class Config:
        from_attributes = True
