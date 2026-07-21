from pydantic import BaseModel


class CityBaseModel(BaseModel):
    name: str
    additional_info: str | None = None


class CityCreateModel(CityBaseModel):
    ...


class CityModel(CityBaseModel):
    id: int
