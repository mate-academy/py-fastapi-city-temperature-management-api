from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CityCreate(BaseModel):
    name: str
    additional_info: str | None = None


class City(CityCreate):
    id: int

    model_config = ConfigDict(
        from_attributes=True,
    )


class Temperature(BaseModel):
    id: int
    city_id: int
    date_time: datetime
    temperature: float

    model_config = ConfigDict(
        from_attributes=True,
    )
