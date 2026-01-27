from typing import Optional

from pydantic import BaseModel, PositiveInt, ConfigDict

class BaseCitySchema(BaseModel):
    name: str
    additional_info: str


class CreateCitySchema(BaseCitySchema):
    pass


class RetrieveCitySchema(BaseCitySchema):
    model_config = ConfigDict(from_attributes=True)
    id: PositiveInt


class UpdateCitySchema(BaseModel):
    name: Optional[str] = None
    additional_info: Optional[str] = None
