from pydantic import BaseModel, Field
from pydantic import ConfigDict


class CityBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    additional_info: str | None = None

class CityCreate(CityBase):
    latitude: float
    longitude: float


class CityUpdate(CityBase):
    name: str | None = None
    latitude: float | None = None
    longitude: float | None = None
    additional_info: str | None = None

class CityRead(CityBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    latitude: float
    longitude: float
