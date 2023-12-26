from pydantic import BaseModel


class CityBase(BaseModel):
    name: str
    additional_info: str | None = None


class CityCreate(CityBase):
    pass


class City(CityBase):
    id: int
    name: str

    class Config:
        orm_mode = True
