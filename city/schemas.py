from pydantic import BaseModel


class CityBase(BaseModel):
    name: str
    additional_info: str


class CityList(CityBase):
    id: int
