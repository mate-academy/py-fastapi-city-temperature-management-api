from datetime import date

from pydantic import BaseModel, ConfigDict


class City(BaseModel):
    name: str
    additional_info: str


class CreateCity(City):
    pass


class CityList(City):
    id: int


class UpdateCity(BaseModel):
    name: str | None = None
    additional_info: str | None = None


class CityDetail(City):
    id: int

    model_config = ConfigDict(from_attributes=True)


class Temperature(BaseModel):
    date_time: date
    temperature: float


class TemperatureCreate(Temperature):
    city_id: int


class TemperatureUpdate(Temperature):
    pass


class TemperatureList(Temperature):
    id: int
    city_id: int


class TemperatureDetail(Temperature):
    id: int
    city_id: int

    model_config = ConfigDict(from_attributes=True)
