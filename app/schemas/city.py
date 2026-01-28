from pydantic import BaseModel, Field


class CityBase(BaseModel):
    name: str = Field(min_length=1, max_length=255)
    additional_info: str | None = Field(default=None, max_length=1000)
    latitude: float
    longitude: float


class CityCreate(CityBase):
    pass


class CityUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=255)
    additional_info: str | None = Field(default=None, max_length=1000)
    latitude: float | None = None
    longitude: float | None = None


class CityRead(CityBase):
    id: int

    class Config:
        from_attributes = True
