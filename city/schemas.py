from pydantic import BaseModel


class CityBase(BaseModel):
    name: str
    additional_info: str


class CityCreate(CityBase):
    pass


class CityDelete(CityBase):
    id: int


class City(CityBase):
    id: int
