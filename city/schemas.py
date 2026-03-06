from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict, Field


class CityBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    additional_info: str | None = Field(default=None, max_length=511)


class CityCreate(CityBase):
    pass


class CityUpdate(CityBase):
    name: Optional[str] = None
    additional_info: Optional[str] = None


class CityRead(CityBase):
    model_config = ConfigDict(
        from_attributes=True,
    )

    id: int
