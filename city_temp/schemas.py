from datetime import datetime

from pydantic import BaseModel, ConfigDict


class CityBase(BaseModel):
    name: str
    additional_info: str | None


class CityCreate(CityBase):
    pass


class CityUpdate(CityBase):
    pass


class CityDelete(BaseModel):
    deleted: bool


class City(CityBase):
    id: int

    model_config = ConfigDict(
        from_attributes=True
    )


class TemperatureBase(BaseModel):
    date_time: datetime
    temperature: float
    city_id: int


class TemperatureCreate(TemperatureBase):
    pass


class Temperature(TemperatureBase):
    id: int

    model_config = ConfigDict(
        from_attributes=True
    )
