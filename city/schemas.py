from pydantic import BaseModel


class CityBase(BaseModel):
    name: str
    additional_info: str


class CityCreate(CityBase):
    pass


class City(CityBase):
    id: int

    class Config:
        from_attributes = True


class CityDelete(BaseModel):
    message: str


class CityName(BaseModel):
    name: str

    class Config:
        from_attributes = True
