from datetime import datetime

from pydantic import BaseModel

class City(BaseModel):
    id: int
    name: str
    additional_info: str


    class Config:
        orm_mode = True


class Temperature(BaseModel):
    id: int
    city_id: int
    date_time: datetime
    temperature: float

    class Config:
        orm_mode = True


class CityCreate(City):
    name: str
    additional_info: str


class CityGet(City):
    pass


class CityUpdate(City):
    pass


class CityDelete(City):
    pass

class TemperatureUpdate(Temperature):
    pass

