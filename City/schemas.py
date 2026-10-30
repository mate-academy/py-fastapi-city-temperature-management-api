from pydantic import BaseModel, ConfigDict


class CityBase(BaseModel):
    name: str
    additional_info: str


class CityCreate(CityBase):
    pass


class CityList(CityBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class CityUpdate(CityBase):
    name: str | None = None
    additional_info: str | None = None