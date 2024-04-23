from pydantic import BaseModel


class CityBase(BaseModel):
    id: int
    name: str
    additional: str


class CityIn(BaseModel):
    name: str
    additional: str
