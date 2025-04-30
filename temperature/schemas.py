from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field

from city.schemas import CityRetrieveSchema


class TemperatureBase(BaseModel):
    date_time: datetime
    temperature: float


class TemperatureCreateSchema(TemperatureBase):
    city_id: int


class TemperatureRetrieveSchema(TemperatureBase):
    id: int
    city: CityRetrieveSchema
    class Config:
        from_attributes = True


class TemperatureListSchema(BaseModel):
    temperatures_list: list[TemperatureRetrieveSchema]
    total_items: int
    total_pages: int
    prev_page: Optional[str]
    next_page: Optional[str]

    class Config:
        from_attributes = True
