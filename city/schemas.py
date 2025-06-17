from typing import Optional

from pydantic import BaseModel, ConfigDict


class CityBase(BaseModel):
    name: str
    additional_info: Optional[str] = None

    model_config = ConfigDict(arbitrary_types_allowed=True)


class CityCreate(CityBase):
    pass


class CityUpdate(CityBase):
    name: str
    additional_info: Optional[str] = None


class City(CityBase):
    id: int

    class Config:
        from_attributes = True
