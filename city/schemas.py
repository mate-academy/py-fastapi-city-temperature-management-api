from pydantic import BaseModel


class CityRead(BaseModel):
    id: int
    name: str
    additional_info: str


class CityCreate(BaseModel):
    name: str
    additional_info: str | None = None
