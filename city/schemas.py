from pydantic import BaseModel


class CityCreate(BaseModel):
    name: str
    additional_info: str


class CityRead(BaseModel):
    name: str


class CityReadDetails(BaseModel):
    id: int
    name: str
    additional_info: str


class CityUpdate(BaseModel):
    name: str
    additional_info: str

    class Config:
        orm_mode = True


class CityDelete(BaseModel):
    id: str
    name: str
    deleted: bool
