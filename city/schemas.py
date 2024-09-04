from typing import Optional

from pydantic import BaseModel, ConfigDict


class CityCreate(BaseModel):
    name: str
    additional_info: Optional[str] = None


class CityResponse(BaseModel):
    id: int
    name: str
    additional_info: Optional[str] = None

    model_config = ConfigDict(
        from_attributes=True
    )
