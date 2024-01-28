from pydantic import BaseModel


class CityBase(BaseModel):
    id: int
    name: str
    additional_info: str


class CityCreate(BaseModel):
    name: str
    additional_info: str


class CityUpdate(BaseModel):
    name: str
    additional_info: str


class City(CityBase):
    id: int

    class Config:
        orm_mode = True


class CityDelete(BaseModel):
    id: int
