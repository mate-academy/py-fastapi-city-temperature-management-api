from typing import Optional

from pydantic import BaseModel, ConfigDict


class CityBase(BaseModel):
    name: str
    additional_info: Optional[str] = None


class CityCreate(CityBase):
    pass


class City(CityBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    latitude: float
    longitude: float


class CityUpdate(CityBase):
    name: Optional[str] = None
    additional_info: Optional[str] = None
