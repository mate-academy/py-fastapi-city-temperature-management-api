from pydantic import BaseModel


class CityCreate(BaseModel):
    name: str
    additional_info: str | None = None


class CityRead(CityCreate):
    id: int


    class Config:
        from_attributes = True