import datetime
from pydantic import BaseModel


class CityBase(BaseModel):
    name: str
    additional_info: str | None = None


class CityCreate(CityBase):
    pass


class CityUpdate(BaseModel):
    name: str | None = None
    additional_info: str | None = None


class City(CityBase):
    id: int

    class Config:
        from_attributes = True
        orm_mode = True


class CityDelete(BaseModel):
    id: int
    deleted: bool = True

    class Config:
        from_attributes = True
        orm_mode = True
