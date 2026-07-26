from datetime import datetime

from pydantic import BaseModel, ConfigDict


class TemperatureBase(BaseModel):
    city_id: int
    date_time: datetime
    temperature: float | None = None
    error_message: str | None = None


class UpdateTemperature(TemperatureBase):
    pass


class Temperature(TemperatureBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
