from datetime import date
from pydantic import BaseModel


class City(BaseModel):
    id: int
    name: str
    additional_info: str | None = None

    class Config:
        from_attributes = True


class CityCreate(City):
    pass


class CityRead(City):
    id: int
    temperatures: list["Temperature"] = []

    class Config:
        orm_mode = True


class Temperature(BaseModel):
    id: int
    city_id: int
    date_time: date
    temperature: float

    class Config:
        from_attributes = True


class TemperatureCreate(Temperature):
    pass


class TemperatureRead(Temperature):
    id: int

    class Config:
        orm_mode = True