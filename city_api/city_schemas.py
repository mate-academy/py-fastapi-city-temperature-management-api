from pydantic import BaseModel


class CityUpdate(BaseModel):
    name: str | None = None
    additional_info: str | None = None


class CityBase(BaseModel):
    name: str
    additional_info: str | None = None


class CityCreate(CityBase):
    pass


class CityDeleteMessage(BaseModel):
    message: str

class City(CityBase):
    id: int

    class Config:

        orm_mode = True