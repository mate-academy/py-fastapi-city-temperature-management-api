from typing import Optional

from pydantic import BaseModel


class CityBase(BaseModel):
    name: str
    additional_info: Optional[str] = None


class CityCreate(CityBase):
    pass


class CityUpdate(BaseModel):
    additional_info: Optional[str] = None


class CityResponse(CityBase):
    id: int

    model_config = {"from_attributes": True}
