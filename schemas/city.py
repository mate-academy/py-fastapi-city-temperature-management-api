from pydantic import BaseModel


class CityBase(BaseModel):
    pass


class CreateCityRequest(CityBase):
    name: str
    additional_info: str | None = None


class CityResponse(CreateCityRequest):
    id: int

    class Config:
        orm_mode = True
