from pydantic import BaseModel


class CityBase(BaseModel):
    name: str


class City(CityBase):
    id: int

    class Config:
        from_attributes = True


class CityCreate(CityBase):
    additional_info: str


class CityDetail(CityBase):
    id: int
    additional_info: str


class Config:
    from_attributes = True


class CityUpdate(CityBase):
    additional_info: str
