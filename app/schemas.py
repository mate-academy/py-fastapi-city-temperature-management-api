from datetime import date
from pydantic import BaseModel


class City(BaseModel):
    name: str
    additional_info: str


class CityCreate(City):
    pass


class CityRead(City):
    id: int
    temperatures: list["Temperature"] = []

    class Config:
        orm_mode = True


class Temperature(BaseModel):
    city_id: int
    date_time: date
    temperature: float


class TemperatureCreate(Temperature):
    pass


class TemperatureRead(Temperature):
    id: int

    class Config:
        orm_mode = True