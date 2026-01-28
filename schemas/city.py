from pydantic import BaseModel, ConfigDict


class CityBase(BaseModel):
    name: str
    additional_info: str


class CityRead(CityBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class CityCreate(CityBase):
    pass


class CityUpdate(BaseModel):
    name: str | None = None
    additional_info: str | None = None
