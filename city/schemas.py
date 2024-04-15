from pydantic import BaseModel


class CityBase(BaseModel):
    name: str
    additional_info: str


class CityCreate(CityBase):
    pass


class CityUpdate(BaseModel):
    name: str = None
    additional_info: str = None


class CityList(CityBase):
    id: int

    class Config:
        from_attributes = True
