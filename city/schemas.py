from typing import Optional

from pydantic import BaseModel, ConfigDict


class CityBase(BaseModel):
    name: str
    additional_info: Optional[str] = None


class CityCreate(CityBase):
    pass


class CityUpdate(BaseModel):
    name: Optional[str] = None
    additional_info: Optional[str] = None

    model_config = ConfigDict(from_attributes=True)


class City(CityBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
