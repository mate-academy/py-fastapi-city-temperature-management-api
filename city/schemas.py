from pydantic import BaseModel


class CityBase(BaseModel):
    name: str
    additional_info: str


class CityCreate(CityBase):
    pass


class City(BaseModel):
    id: int
    name: str
    additional_info: str

    class Config:
        orm_mode = True
