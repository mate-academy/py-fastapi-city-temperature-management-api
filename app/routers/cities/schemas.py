from typing import Optional

from pydantic import BaseModel


class CityIn(BaseModel):
    name: str
    additional_info: Optional[str] | None = None


class CityOut(BaseModel):
    id: int
    name: str
    additional_info: Optional[str] | None = None

    model_config = {"from_attributes": True}