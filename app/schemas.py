from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CityBase(BaseModel):
    name: str
    additional_info: str | None = None
    latitude: float
    longitude: float


class CityCreate(CityBase):
    pass


class CityResponse(CityBase):
    id: int  # noqa: VNE003

    model_config = ConfigDict(from_attributes=True)


class TemperatureBase(BaseModel):
    city_id: int
    date_time: datetime
    temperature: float


class TemperatureResponse(TemperatureBase):
    id: int  # noqa: VNE003

    model_config = ConfigDict(from_attributes=True)
