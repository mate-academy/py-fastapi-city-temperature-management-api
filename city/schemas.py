from typing import List

from pydantic import BaseModel, ConfigDict


class CityBase(BaseModel):
    name: str
    additional_info: str

    model_config = ConfigDict(from_attributes=True)


# --- Requests ---
class CityCreateRequest(CityBase):
    pass


# --- Responses ---
class CityResponse(CityBase):
    id: int


class CityListResponse(BaseModel):
    cities: List[CityResponse]


class MessageResponse(BaseModel):
    msg: str
