from datetime import datetime

from pydantic import BaseModel, ConfigDict


class TemperatureBase(BaseModel):
    city_id: int
    temperature: float


class CityShort(BaseModel):
    name: str

    model_config = ConfigDict(from_attributes=True)


class Temperature(TemperatureBase):
    id: int
    date_time: datetime
    city: CityShort

    model_config = ConfigDict(from_attributes=True)


class TemperatureCreate(TemperatureBase):
    pass


class TemperatureOut(TemperatureBase):
    id: int
    date_time: datetime
    city: CityShort

    class Config:
        from_attributes = True
