from pydantic import BaseModel


class CityCreate(BaseModel):
    name: str
    additional_info: str = None


class CityRead(BaseModel):
    id: int
    name: str
    additional_info: str

    class Config:
        orm_mode = True
