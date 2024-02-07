from pydantic import BaseModel


class CityBase(BaseModel):
    name: str
    additional_info: str = None


class CityCreate(CityBase):
    pass


class CityUpdate(CityBase):
    pass


class City(CityBase):
    id: int

    class Config:
        orm_mode = True
