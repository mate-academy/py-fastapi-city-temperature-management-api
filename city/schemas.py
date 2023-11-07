from pydantic import BaseModel


class CityBase(BaseModel):
    name: str
    additional_info: str


class DeleteCity(BaseModel):
    id: int


class CityCreate(CityBase):
    pass


class City(CityBase):
    id: int

    class Config:
        from_attributes = True
