from pydantic import BaseModel


class CityBase(BaseModel):
    name: str
    additional_info: str

    class Config:
        from_attributes = True


class CityCreate(CityBase):
    pass


class CityRead(BaseModel):
    id: int
    name: str
    additional_info: str

    class Config:
        from_attributes = True


class CityUpdate(BaseModel):
    name: str | None = None
    additional_info: str | None = None

    class Config:
        from_attributes = True
