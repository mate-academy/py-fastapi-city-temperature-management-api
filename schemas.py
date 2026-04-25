from pydantic import BaseModel, ConfigDict
from datetime import datetime
from typing import Optional


# City Schemas
class CityBase(BaseModel):
    name: str
    additional_info: Optional[str] = None


class CityCreate(CityBase):
    pass


class CityUpdate(BaseModel):
    name: Optional[str] = None
    additional_info: Optional[str] = None


class City(CityBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


# Temperature Schemas
class TemperatureBase(BaseModel):
    city_id: int
    temperature: float


class TemperatureCreate(TemperatureBase):
    date_time: Optional[datetime] = None


class Temperature(TemperatureBase):
    id: int
    date_time: datetime
    model_config = ConfigDict(from_attributes=True)


# Response with city name
class TemperatureWithCity(Temperature):
    city_name: str


class TemperatureUpdateResponse(BaseModel):
    message: str
    updated_cities: int
    details: list[dict]
