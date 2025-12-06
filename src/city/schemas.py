from pydantic import BaseModel


class CityBase(BaseModel):
    name: str
    additional_info: str | None


class CityCreate(CityBase):
    pass


class CityUpdate(BaseModel):
    name: str | None
    additional_info: str | None


class City(CityBase):
    id: int

    class Config:
        from_attributes = True
