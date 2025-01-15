from datetime import datetime

from pydantic import BaseModel


class CityBase(BaseModel):
    name: str
    additional_info: str


class CityCreate(CityBase):
    pass


class CityUpdate(CityBase):
    pass


class City(CityBase):
    id: int

    class Config:
        orm_mode = True


class Temperature(BaseModel):
    city_id: int
    date_time: datetime
    temperature: float



class TemperatureUpdate(Temperature):
    pass

class TemperaturesList(Temperature):
    id: int

    class Config:
        orm_mode = True