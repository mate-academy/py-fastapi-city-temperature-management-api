from pydantic import BaseModel


class City(BaseModel):
    name: str
    additional: str


class CityList(City):
    id: int
