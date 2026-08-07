from pydantic import BaseModel


class CityBase(BaseModel):
    name: str
    additional_info: str


class CityCreate(CityBase):
    pass


class CityUpdate(CityBase):
    name: str | None = None
    additional_info: str | None = None


class CityDetail(CityBase):
    pass


class CityList(CityBase):
    pass
