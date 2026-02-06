from datetime import datetime

from pydantic import BaseModel, ConfigDict



class TemperatureBase(BaseModel):
    city_id: int
    date_time: datetime
    temperature: float


class Temperature(TemperatureBase):
    id: int

    class Config:
        model_config = ConfigDict(from_attributes=True)


class TemperatureCreate(TemperatureBase):
    pass


class TemperatureUpdate(TemperatureBase):
    pass


class TemperaturePatch(BaseModel):
    date_time: datetime | None = None
    temperature: float | None = None


class TemperatureDelete(TemperatureBase):
    pass
