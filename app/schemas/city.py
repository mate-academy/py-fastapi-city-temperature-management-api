from pydantic import BaseModel
from pydantic import ConfigDict


class CityCreate(BaseModel):
    name: str
    additional_info: str


class CityResponse(CityCreate):
    id: int

    model_config = ConfigDict(from_attributes=True)
