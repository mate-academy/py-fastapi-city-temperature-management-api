from datetime import datetime

from pydantic import BaseModel

from city.schemas import CityResponse


class TemperatureBase(BaseModel):
    temperature: float
    date_time: datetime

    model_config = {"from_attributes": True}


class TemperatureRequest(TemperatureBase):
    city_id: int


class TemperatureResponse(TemperatureBase):
    id: int
    city_id: int


class TemperatureDetailResponse(TemperatureBase):
    id: int
    city: CityResponse
