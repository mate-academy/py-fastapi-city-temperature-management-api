from pydantic import BaseModel


class CityBase(BaseModel):
    name: str
    country: str
    additional_info: str


class City(CityBase):
    id: int

    class Config:
        from_attributes = True
