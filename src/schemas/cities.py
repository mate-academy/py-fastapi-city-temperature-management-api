from pydantic import BaseModel, ConfigDict


class CityBaseModel(BaseModel):
    name: str
    additional_info: str


class CityCreate(CityBaseModel):
    pass


class City(CityBaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
