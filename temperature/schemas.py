from datetime import datetime

from pydantic import BaseModel


class CityBase(BaseModel):
    name: str
    additional_info: str

class CityCreate(CityBase):
    pass

class City(CityBase):
    id: int

    class Config:
        orm_mode = True



class TemperatureBase(BaseModel):
    date_time: datetime
    temperature: float

class TemperatureCreate(TemperatureBase):
    city_id: int

class Temperature(TemperatureBase):
    id: int
    city_id: int

    class Config:
        orm_mode = True
