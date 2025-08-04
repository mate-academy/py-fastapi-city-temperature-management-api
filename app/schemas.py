from datetime import datetime
from typing import Optional, List

from pydantic import BaseModel


class MessageSchema(BaseModel):
    message: str


class CityBaseSchema(BaseModel):
    name: str
    additional_info: Optional[str]


class CityCreateSchema(CityBaseSchema):
    pass


class CityUpdateSchema(CityBaseSchema):
    name: Optional[str] = None
    additional_info: Optional[str] = None


class CityListSchema(CityBaseSchema):
    id: int

    class Config:
        from_attributes = True


class CityRetrieveSchema(CityListSchema):
    temperatures: List["TemperatureListSchema"]


class TemperatureBaseSchema(BaseModel):
    city_id: int
    date_time: datetime
    temperature: float


class TemperatureCreateSchema(TemperatureBaseSchema):
    pass


class TemperatureListSchema(TemperatureBaseSchema):
    id: int

    class Config:
        from_attributes = True


class TemperatureRetrieveSchema(BaseModel):
    date_time: datetime
    temperature: float
    city: CityBaseSchema

    class Config:
        from_attributes = True
