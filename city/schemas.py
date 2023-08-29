from pydantic import BaseModel


class CityBase(BaseModel):
    name: str


class CityCreate(CityBase):
    additional_info: str


class City(CityBase):
    id: int

    class Config:
        from_attributes = True


class CityDetail(CityBase):
    id: int
    name: str
    additional_info: str

    class Config:
        from_attributes = True
