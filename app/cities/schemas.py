from pydantic import BaseModel, ConfigDict, Field


class CityBase(BaseModel):
    name: str = Field(..., max_length=100)
    additional_info: str | None = Field(default=None, max_length=500)


class CityCreate(CityBase):
    pass


class CityUpdate(BaseModel):
    name: str | None = Field(default=None, max_length=100)
    additional_info: str | None = Field(default=None, max_length=500)


class CityResponse(CityBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
