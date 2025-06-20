from datetime import datetime

from pydantic import BaseModel, ConfigDict


class TemperatureBaseSchema(BaseModel):
    date_time: datetime
    temperature: float

    model_config = ConfigDict(from_attributes=True)


class TemperatureResponseSchema(TemperatureBaseSchema):
    id: int
    city_id: int


class MessageResponseSchema(BaseModel):
    message: str
