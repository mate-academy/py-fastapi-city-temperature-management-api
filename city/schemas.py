from typing import Optional

from pydantic import BaseModel


class CityBase(BaseModel):
    name: str
    additional_info: Optional[str] = None

    model_config = {"from_attributes": True}


class CityRequest(CityBase):
    pass


class CityResponse(CityBase):
    id: int
