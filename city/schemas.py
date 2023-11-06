from pydantic import BaseModel


class CityBase(BaseModel):
    name: str
    additional_info: str

    class Config:
        orm_mode = True


class CityCreateUpdate(CityBase):
    pass


class CityRead(CityBase):
    id: int
