from datetime import datetime

from pydantic import BaseModel, ConfigDict, field_validator
from city.schemas import City


class BaseTemperature(BaseModel):
    date_time: datetime
    temperature: float
    city_id: int


class TemperatureCreate(BaseTemperature):
    pass


class Temperature(BaseTemperature):
    id: int
    city: str

    model_config = ConfigDict(from_attributes=True)

    @field_validator("city", mode="before")
    @classmethod
    def get_city_name(cls, inst):
        if hasattr(inst, "name"):
            return inst.name
        return inst
