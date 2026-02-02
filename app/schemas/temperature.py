from datetime import datetime

from pydantic import BaseModel, ConfigDict


class TemperatureRead(BaseModel):
    id: int
    city_id: int
    date_time: datetime
    temperature: float

    model_config = ConfigDict(from_attributes=True)


class TemperatureUpdateResult(BaseModel):
    total_cities: int
    stored: int
    failed_city_ids: list[int] = []
