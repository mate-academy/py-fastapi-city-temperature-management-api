from pydantic import BaseModel, ConfigDict


class CityBase(BaseModel):
    name: str
    additional_info: str | None = None


class City(CityBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class CityCreate(CityBase):
    pass
