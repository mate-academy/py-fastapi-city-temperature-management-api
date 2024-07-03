from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class CityBase(BaseModel):
    name: str = Field(..., example="City Name")
    additional_info: Optional[str] = None

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "name": "City Name",
                "additional_info": "Additional information about the city"
            }
        }


class City(CityBase):
    id: int

    class Config:
        orm_mode = True


class CityCreate(CityBase):
    pass


class CityUpdate(BaseModel):
    name: Optional[str] = Field(None, example="Updated City Name")
    additional_info: Optional[str] = None

    class Config:
        orm_mode = True


class TemperatureBase(BaseModel):
    city_id: int
    temperature: float

    class Config:
        orm_mode = True
        schema_extra = {
            "example": {
                "city_id": 1,
                "temperature": 20.5
            }
        }


class Temperature(TemperatureBase):
    id: int
    date_time: datetime

    class Config:
        orm_mode = True
