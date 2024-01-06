from pydantic import BaseModel


class CityIn(BaseModel):
    name: str
    additional_info: str


class City(CityIn):
    id: int
    name: str
    additional_info: str

    class Config:
        orm_mode = True
