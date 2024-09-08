from datetime import datetime

from pydantic import BaseModel, ConfigDict

from city.schemas import CitySchema


class TemperatureBaseSchema(BaseModel):
    city_id: int
    date_time: datetime | None
    temperature: float | None


class TemperatureCitySchema(TemperatureBaseSchema):
    id: int
    city: CitySchema

    model_config = ConfigDict(from_orm=True)


class TemperatureCreateSchema(TemperatureBaseSchema):
    pass
