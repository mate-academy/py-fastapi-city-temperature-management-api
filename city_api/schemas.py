from typing import Optional

from pydantic import BaseModel, ConfigDict


class CityBaseSchema(BaseModel):
    name: str
    additional_info: str = ""


class CityListSchema(BaseModel):
    id: int
    name: str

    model_config = ConfigDict(from_attributes=True)


class CityUpdateSchema(BaseModel):
    name: Optional[str] = None
    additional_info: Optional[str] = None


class CitySchema(CityBaseSchema):
    id: int

    model_config = ConfigDict(from_attributes=True)
