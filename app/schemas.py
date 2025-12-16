import datetime

from pydantic import BaseModel, ConfigDict

from app.models import City


class CityBaseSchema(BaseModel):
    name: str
    additional_info: str


class CityCreateSchema(CityBaseSchema):
    pass


class CityListSchema(CityBaseSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int


class TemperatureBaseSchema(BaseModel):
    date_time: datetime.datetime
    temperature: float


class TemperatureCreateSchema(TemperatureBaseSchema):
    city_id: int


class TemperatureListSchema(TemperatureBaseSchema):
    model_config = ConfigDict(from_attributes=True)

    id: int
    city: CityListSchema
