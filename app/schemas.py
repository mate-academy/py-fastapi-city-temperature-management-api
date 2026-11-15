from datetime import datetime
from zoneinfo import ZoneInfo

from pydantic import BaseModel, ConfigDict, Field, field_serializer

KYIV_TZ = ZoneInfo("Europe/Kyiv")


class CityBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=200)
    additional_info: str = ""


class CityCreate(CityBase):
    pass


class CityUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=200)
    additional_info: str | None = None


class City(CityBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class Temperature(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    city_id: int
    date_time: datetime
    temperature: float

    @field_serializer("date_time")
    def serialize_date_time(self, value: datetime) -> str:
        if value.tzinfo is None:
            value = value.replace(tzinfo=KYIV_TZ)
        return value.isoformat()



class TemperatureUpdateResult(BaseModel):
    temperatures: list[Temperature]
    errors: list[str] = []
