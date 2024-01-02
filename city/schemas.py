from pydantic import BaseModel


class BaseCity(BaseModel):
    name: str
    additional_info: str


class CityCreate(BaseCity):
    pass


class City(BaseCity):
    id: int

    class Config:
        from_attributes = True
