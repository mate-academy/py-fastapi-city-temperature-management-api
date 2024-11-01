from pydantic import BaseModel


class CityBase(BaseModel):
    name: str
    additional_info: str


class City(BaseModel):
    id: int
    name: str
    additional_info: str = None

    class Config:
        orm_mode = True
