from pydantic import BaseModel


class CityBase(BaseModel):
    name: str
    additional_info: str


class CityCreate(CityBase):
    pass


class CityUpdate(CityBase):
    id: int


class CityDelete(CityBase):
    id: int


class City(CityBase):
    id: str

    class Config:
        orm_mode = True
