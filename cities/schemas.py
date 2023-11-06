from pydantic import BaseModel

from temperature.schemas import TemperatureNested, Temperature


class CityBase(BaseModel):
    name: str
    description: str


class CityCreate(CityBase):
    ...


class CityUpdate(CityBase):
    ...


class City(CityBase):
    id: int
    temperatures: list[TemperatureNested] | None = None

    class Config:
        from_attributes = True


class CityDetail(CityBase):
    id: int
    temperatures: list[Temperature] | None = None

    class Config:
        from_attributes = True
