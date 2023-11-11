from pydantic import BaseModel


class CityCreate(BaseModel):
    name: str
    additional_info: str


class City(CityCreate):
    id: int
