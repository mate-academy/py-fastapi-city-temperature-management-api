from typing import Optional

from pydantic import BaseModel


class CreateCity(BaseModel):
    name: str
    additional_info: str


class ListCity(BaseModel):
    id: int
    name: str
    additional_info: str


class UpdateCity(BaseModel):
    name: Optional[str] = None
    additional_info: Optional[str] = None


class DeleteCity(BaseModel):
    deleted_city:  str
