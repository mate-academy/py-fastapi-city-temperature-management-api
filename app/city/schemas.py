from typing import Optional

from pydantic import BaseModel, ConfigDict, Field, field_validator


class CityBase(BaseModel):
    name: str = Field(min_length=1, max_length=255, examples=["Kyiv"])
    additional_info: Optional[str] = Field(
        default=None, examples=["Capital of Ukraine"]
    )


class CityCreate(CityBase):
    pass


class CityUpdate(BaseModel):
    """All fields are optional: only the provided ones are updated."""

    name: Optional[str] = Field(default=None, min_length=1, max_length=255)
    additional_info: Optional[str] = None

    @field_validator("name")
    @classmethod
    def name_not_null(cls, value: Optional[str]) -> str:
        if value is None:
            raise ValueError("name cannot be null")
        return value


class City(CityBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
