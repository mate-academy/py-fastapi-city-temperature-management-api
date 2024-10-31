from pydantic import BaseModel


class CityBase(BaseModel):
    name: str
    additional_info: str


class CityName(BaseModel):
    name: str


class CityCreate(CityBase):
    pass


class CityUpdate(CityBase):
    pass


class City(CityBase):
    id: int

    class Config:
        from_attributes = True
