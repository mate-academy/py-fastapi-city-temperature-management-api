from pydantic import BaseModel


class CityBase(BaseModel):
    name: str
    additional_info: str


class CityBaseCreate(CityBase):
    pass


class City(CityBase):
    id: int

    class Config:
        orm_mode = True
