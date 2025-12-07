from pydantic import BaseModel, ConfigDict
from typing import Optional


class CityBase(BaseModel):
    name: str
    additional_info: Optional[str] = None

class CityCreate(CityBase):
    pass

class CityUpdate(BaseModel):
    """
    Schema for updating a city. All fields are optional to allow partial updates.
    """
    name: Optional[str] = None
    additional_info: Optional[str] = None

class City(CityBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
