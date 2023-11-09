from pydantic import BaseModel


class CityBase(BaseModel):
    name: str
    aditional_info: str


class CityCreate(CityBase):
    ...


class City(CityBase):
    id: int

    class Config:
        from_attributes = True
