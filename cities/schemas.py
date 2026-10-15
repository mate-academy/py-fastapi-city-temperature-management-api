from pydantic import BaseModel, ConfigDict
from temperatures.schemas import TemperatureSchema


class CityBase(BaseModel):
    name: str
    additional_info: str | None = None


class CityCreate(CityBase):
    pass


class CityUpdate(CityBase):
    pass


class City(CityBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class CityDetail(City):
    temperatures: list[TemperatureSchema] = []
