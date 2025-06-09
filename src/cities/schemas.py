from pydantic import BaseModel


class CityNew(BaseModel):
    name: str
    additional_info: str | None = None


class City(BaseModel):
    id: int
    name: str
    additional_info: str | None

    class Config:
        from_attributes = True
