from pydantic import BaseModel, Field, ConfigDict


class CityBase(BaseModel):
    name: str = Field(max_length=127)
    additional_info: str | None = None


class CityCreate(CityBase):
    pass


class CityUpdate(CityBase):
    name: str | None = Field(max_length=127, default=None)


class CityRead(CityBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
