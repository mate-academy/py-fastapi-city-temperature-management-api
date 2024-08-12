from typing import Optional

from pydantic import BaseModel


class CitySchema(BaseModel):
    name: str
    additional_info: Optional[str]


class CityListSchema(CitySchema):
    id: int

    class Config:
        from_attributes = True


class CityCreateSchema(CitySchema):
    pass
