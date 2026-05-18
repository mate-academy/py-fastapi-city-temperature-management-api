from pydantic import BaseModel


class CityRead(BaseModel):
    id: int
    name: str
    additional_info: str

    class Config:
        from_attributes = True


class CityCreate(BaseModel):
    name: str
    additional_info: str
