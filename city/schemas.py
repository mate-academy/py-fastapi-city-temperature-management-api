from pydantic import BaseModel


class CityBase(BaseModel):
    name: str
    additional_info: str


class City(CityBase):
    id: int
