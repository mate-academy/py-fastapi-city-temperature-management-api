from pydantic import BaseModel


class CityBase(BaseModel):
    name: str
    additional_info: str | None


class CreateCity(CityBase):
    pass


class UpdateCity(BaseModel):
    id: int
    name: str | None
    additional_info: str | None


class City(BaseModel):
    id: int
