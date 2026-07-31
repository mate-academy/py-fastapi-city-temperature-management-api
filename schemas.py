from datetime import datetime
from pydantic import BaseModel, ConfigDict

class CityBase(BaseModel):
    name: str
    additional_info: str

class CityCreate(CityBase):
    pass

class TemperatureBase(BaseModel):
    date_time: datetime
    temperature: float

class TemperatureCreate(TemperatureBase):
    city_id: int

class Temperature(TemperatureBase):
    model_config = ConfigDict(from_attributes=True)
    city_id: int
    id: int

class City(CityBase):
    model_config = ConfigDict(from_attributes=True)
    id: int
