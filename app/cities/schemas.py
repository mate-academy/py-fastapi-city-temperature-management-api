from pydantic import BaseModel


class CityBase(BaseModel):
    name: str
    additional_info: str | None = None


class CityCreate(CityBase):
    pass


class CityUpdate(CityBase):
    name: str | None = None


class CityResponse(CityBase):
    id: int

    class Config:
        from_attributes = True
