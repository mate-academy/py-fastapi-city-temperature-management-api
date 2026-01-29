from pydantic import BaseModel, ConfigDict


class CityBase(BaseModel):
    """Base schema for city data."""

    name: str
    additional_info: str | None = None


class CityCreate(CityBase):
    """Schema for creating a new city."""

    pass


class City(CityBase):
    """Schema for returning city data, including its ID."""

    model_config = ConfigDict(from_attributes=True)

    id: int


class CityUpdate(CityBase):
    """Schema for updating an existing city."""

    name: str | None
    additional_info: str | None
