from pydantic import BaseModel


class CityBase(BaseModel):
    name: str
    additional_info: str

    class Config:
        from_attributes = True


class CityCreate(CityBase):
    pass


class CityUpdate(CityCreate):
    pass


class CityUpdatePartial(CityCreate):
    name: str | None = None
    additional_info: str | None = None


class City(CityBase):
    id: int

    class Config:
        from_attributes = True
