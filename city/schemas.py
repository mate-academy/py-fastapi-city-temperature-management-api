from pydantic import BaseModel


class CityBase(BaseModel):
    name: str
    additional_info: str

    class Config:
        from_attributes = True


class CityCreateUpdate(CityBase):
    pass


class CityRead(CityBase):
    id: int
