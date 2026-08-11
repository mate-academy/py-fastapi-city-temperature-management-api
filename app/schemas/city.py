from pydantic import BaseModel, ConfigDict


class City(BaseModel):
    name: str
    additional_info: str | None = None


class CityCreate(City):
    pass


class CityRead(City):
    id: int
    model_config = ConfigDict(from_attributes=True)
