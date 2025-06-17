from typing import Optional

from pydantic import BaseModel


class CityBaseSchema(BaseModel):
    name: str
    additional_info: Optional[str] = None


class CityCreateSchema(CityBaseSchema):
    pass


class CityReadSchema(CityBaseSchema):
    id: int


class MessageResponse(BaseModel):
    message: str
