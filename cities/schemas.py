from pydantic import BaseModel, Field, ConfigDict


class City(BaseModel):
    name: str = Field(max_length=127)
    additional_info: str | None = None


class CityCreate(City):
    pass


class CityUpdate(City):
    name: str | None = Field(max_length=127, default=None)


class CityRead(City):
    id: int

    model_config = ConfigDict(from_attributes=True)
