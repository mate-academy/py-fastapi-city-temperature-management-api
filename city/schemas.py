from pydantic import BaseModel, ConfigDict

from temperature.schemas import Temperature


class CityBase(BaseModel):
    name: str
    additional_info: str | None = None


class CityCreate(CityBase):
    pass


class City(CityBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    temperatures: list[Temperature]
