from pydantic import BaseModel


class CityBase(BaseModel):
    name: str
    additional_info: str | None = None


class City(CityBase):
    id: int

    class Config:
        orm_mode = True


class CityCreate(CityBase):
    pass


class CityUpdate(BaseModel):
    name: str | None = None
    additional_info: str | None = None
