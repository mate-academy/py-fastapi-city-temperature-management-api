from pydantic import BaseModel

from temperature.schemas import Temperature


class CityBase(BaseModel):
    name: str

class CityCreate(CityBase):
    pass

class City(CityBase):
    id: int
    additional_info: list[Temperature]

    class Config:
        orm_mode = True
