from pydantic import BaseModel


class CityBaseModel(BaseModel):
    name: str
    additional_info: str


class CityCreateModel(CityBaseModel):
    ...


class CityListRetrieveModel(CityBaseModel):
    id: int
