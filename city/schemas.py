from pydantic import BaseModel, ConfigDict


class CityBase(BaseModel):
    name: str
    additional_info: str

    model_config = ConfigDict(from_attributes=True)

class City(CityBase):
    model_config = ConfigDict(from_attributes=True)

    id: int

class CityCreate(CityBase):
    pass

class CityUpdate(CityBase):
    name: str | None = None
    additional_info: str | None = None
