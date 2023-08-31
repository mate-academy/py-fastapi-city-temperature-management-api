from pydantic import BaseModel


class CityBase(BaseModel):
    name: str
    additional_info: str


class City(CityBase):
    id: int

    class Config:
        from_attributes = True


class CityCreate(CityBase):
    pass


class CityUpdate(CityBase):
    name: str
    additional_info: str
