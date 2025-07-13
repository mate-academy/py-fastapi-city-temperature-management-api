from datetime import datetime
from typing import Optional

from pydantic import BaseModel


class CityDtoBase(BaseModel):
    name: str
    additional_info: Optional[str] = None


class CityDtoCreate(CityDtoBase):
    pass


class CityDto(CityDtoBase):
    id: int

    class Config:
        orm_mode = True


class TemperatureDtoBase(BaseModel):
    temperature: float


class TemperatureDtoCreate(BaseModel):
    temperature: float
    city_id: int


class TemperatureDto(TemperatureDtoBase):
    id: int
    date_time: datetime
    city: CityDtoBase

    class Config:
        orm_mode = True
