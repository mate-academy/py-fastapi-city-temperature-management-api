from datetime import datetime

from pydantic import BaseModel, ConfigDict


class TemperatureBase(BaseModel):
    """Base schema for temperature data."""

    date_time: datetime
    temperature: float
    city_id: int


class TemperatureCreate(TemperatureBase):
    """Schema for creating a new temperature record."""

    pass


class Temperature(TemperatureBase):
    """Schema for returning temperature data, including its ID."""

    model_config = ConfigDict(from_attributes=True)

    id: int
