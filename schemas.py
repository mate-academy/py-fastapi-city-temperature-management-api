from datetime import datetime
from typing import Optional

from pydantic import BaseModel, ConfigDict


class CityBaseSchema(BaseModel):
    name: str
    additional_info: str


class CityListSchema(CityBaseSchema):
    id: int

    model_config = ConfigDict(from_attributes=True)


class CityCreateSchema(CityBaseSchema):
    pass


class CityUpdateSchema(BaseModel):
    name: Optional[str] = None
    additional_info: Optional[str] = None


class TemperatureBaseSchema(BaseModel):
    city_id: int
    date_time: datetime
    temperature: float


class TemperatureListSchema(TemperatureBaseSchema):
    id: int

    model_config = ConfigDict(from_attributes=True)
