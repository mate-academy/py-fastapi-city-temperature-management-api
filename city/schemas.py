from pydantic import BaseModel


class CityBase(BaseModel):
    name: str
    additional_info: str


class CityCreate(CityBase):
    pass


class CityDelete(BaseModel):
    id: int


class City(CityBase):
    id: int

    class Config:
        orm_mode = True
