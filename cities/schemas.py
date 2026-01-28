
from pydantic import BaseModel, Field, ConfigDict


class CityBase(BaseModel):
    name: str = Field(min_length=1, max_length=100)
    additional_info: str = Field(min_length=1, max_length=300)
    latitude: float
    longitude: float


class CityCreate(CityBase):
    pass


class CityRead(CityBase):
    id: int
    model_config = ConfigDict(from_attributes=True)
