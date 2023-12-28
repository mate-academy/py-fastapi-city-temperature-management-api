from pydantic import BaseModel


class City(BaseModel):
    id: int
    name: str
    additional_info: str


class CityCreate(BaseModel):
    name: str
    additional_info: str
