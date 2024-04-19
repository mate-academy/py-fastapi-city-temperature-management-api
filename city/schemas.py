from pydantic import BaseModel


class CityBase(BaseModel):
    name: str
    additional_info: str


class CityCreate(CityBase):
    pass


class CityList(BaseModel):
    id: int
    name: str

    class Config:
        from_attributes = True


class CityDetail(CityBase):
    id: int
