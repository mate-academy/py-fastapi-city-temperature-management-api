from pydantic import BaseModel, ConfigDict, Field


class BaseCity(BaseModel):
    name: str = Field(max_length=255)
    additional_info: str = Field(max_length=500)

    model_config = ConfigDict(extra="forbid")


class CityCreate(BaseCity):
    pass


class CityEdit(BaseCity):
    name: str | None = Field(max_length=255, default=None)
    additional_info: str | None = Field(max_length=500, default=None)


class City(BaseCity):
    id: int

    model_config = ConfigDict(from_attributes=True)
