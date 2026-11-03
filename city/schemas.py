from pydantic import BaseModel, ConfigDict


class CityBase(BaseModel):
    name: str
    additional_info: str


class CityCreate(CityBase):
    pass


class CityRead(CityBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    additional_info: str
