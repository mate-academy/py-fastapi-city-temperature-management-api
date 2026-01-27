from datetime import datetime

from typing import Optional

from pydantic import BaseModel, PositiveInt, ConfigDict


class BaseTemperatureSchema(BaseModel):
    temperature: int


class CreateTemperatureSchema(BaseTemperatureSchema):
    city_id: int


class RetrieveTemperatureSchema(BaseTemperatureSchema):
    model_config = ConfigDict(from_attributes=True)
    id: PositiveInt
    date_time: datetime
    city_id: int


class UpdateTemperatureSchema(BaseTemperatureSchema):
    date_time: Optional[datetime] = None
    temperature: Optional[int] = None
