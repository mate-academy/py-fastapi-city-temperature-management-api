from pydantic import BaseModel


class CityBase(BaseModel):
    name: str
    additional_info: str


class CityCreate(CityBase):
    pass


class City(CityBase):
    id: int

    class Config:
        orm_mode = True


class CityUpdate(CityBase):
    name: str | None = None
    additional_info: str | None = None
