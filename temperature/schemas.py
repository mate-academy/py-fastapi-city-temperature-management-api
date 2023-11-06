from datetime import datetime

from pydantic import BaseModel

from city.schemas import CityRead


class TemperatureBase(BaseModel):
    date_time: datetime
    temperature: float

    class Config:
        orm_mode = True


class TemperatureRead(TemperatureBase):
    id: int
    city: CityRead


class TemperatureCreateUpdate(TemperatureBase):
    city_id: int
