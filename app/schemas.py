from pydantic import BaseModel, Field
from datetime import datetime
from typing import Optional


class CityBase(BaseModel):
    name: str = Field(..., min_length=1, description="Name of the city")
    additional_info: Optional[str] = Field(None, description="Additional information about the city")


class CityCreate(CityBase):
    pass


class CityUpdate(BaseModel):
    name: Optional[str] = Field(None, min_length=1, description="Name of the city")
    additional_info: Optional[str] = Field(None, description="Additional information about the city")


class City(CityBase):
    id: int = Field(..., description="Unique identifier for the city")

    class Config:
        from_attributes = True


class TemperatureBase(BaseModel):
    city_id: int = Field(..., description="Reference to the city")
    temperature: float = Field(..., description="Recorded temperature")


class TemperatureCreate(TemperatureBase):
    date_time: Optional[datetime] = Field(None, description="Date and time when the temperature was recorded")


class Temperature(TemperatureBase):
    id: int = Field(..., description="Unique identifier for the temperature record")
    date_time: datetime = Field(..., description="Date and time when the temperature was recorded")

    class Config:
        from_attributes = True


class TemperatureWithCity(Temperature):
    city: City = Field(..., description="City information")

    class Config:
        from_attributes = True

