from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import datetime

class CityBase(BaseModel):
    name: str
    additional_info: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class CityCreate(CityBase):
    pass

class CityUpdate(BaseModel):
    name: Optional[str] = None
    additional_info: Optional[str] = None
    latitude: Optional[float] = None
    longitude: Optional[float] = None

class CityOut(CityBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

class TemperatureBase(BaseModel):
    city_id: int
    temperature: float

class TemperatureOut(TemperatureBase):
    id: int
    date_time: datetime

    model_config = ConfigDict(from_attributes=True)
