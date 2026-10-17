from pydantic import BaseModel, Field, field_validator, ConfigDict
from datetime import datetime


class CityBase(BaseModel):
    name: str = Field(max_length=255)
    additional_info: str | None = Field(default=None, max_length=1000)

    @field_validator('name')
    @classmethod
    def remove_extra_spaces(cls, value: str) -> str:
        value = " ".join(value.split())

        if value == "":
            raise ValueError("The city name cannot be empty")

        return value

class CityCreate(CityBase):
    pass

class CityUpdate(BaseModel):
    name: str | None = Field(default=None, max_length=255)
    additional_info : str | None = Field(default=None, max_length=1000)

class CityResponse(CityBase):
    id: int
    model_config = ConfigDict(from_attributes=True)

class TemperatureBase(BaseModel):
    city_id: int 
    temperature: float

class TemperatureCreate(TemperatureBase):
    pass

class TemperatureResponse(TemperatureBase):
    id: int
    date_time: datetime
    model_config = ConfigDict(from_attributes=True)