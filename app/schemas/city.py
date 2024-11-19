from pydantic import BaseModel


class CityBase(BaseModel):
    name: str
    additional_info: str | None = None


class CityCreate(CityBase):
    pass


class CityRead(CityBase):
    id: int

    class Config:
        from_attributes = True


class CityUpdate(CityBase):
    pass
