from pydantic import BaseModel


class City(BaseModel):
    id: int
    name: str
    additional_info: str | None = None

    class Config:
        from_attributes = True


class CityCreate(BaseModel):
    name: str
    additional_info: str | None = None
