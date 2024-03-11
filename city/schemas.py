from pydantic import BaseModel


class CityBase(BaseModel):
    name: str
    additional_info: str | None


class CreateCity(CityBase):
    pass


class City(BaseModel):
    id: int
