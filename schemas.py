from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


# -----------------
# CITY SCHEMAS
# -----------------
class CityBase(BaseModel):
    name: str
    additional_info: Optional[str] = None


class CityCreate(CityBase):
    pass


class CityRead(CityBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


# -----------------
# TEMPERATURE SCHEMAS
# -----------------
class TemperatureBase(BaseModel):
    city_id: int
    date_time: datetime
    temperature: float


class TemperatureCreate(TemperatureBase):
    pass


class TemperatureRead(TemperatureBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
