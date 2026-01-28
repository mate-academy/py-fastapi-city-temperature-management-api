from pydantic import BaseModel, ConfigDict


class CityBase(BaseModel):
    name: str
    additional_info: str | None = None


class CityCreate(CityBase):
    pass


class CityRead(CityBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
