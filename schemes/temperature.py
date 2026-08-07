from datetime import datetime
from typing import Annotated

from fastapi import Depends
from pydantic import BaseModel


class TemperatureBase(BaseModel):
    city_id: int
    temperature: float
    date_time: datetime


class TemperatureCreate(TemperatureBase):
    pass


class TemperatureDetail(TemperatureBase):
    id: int


class TemperatureUpdate(TemperatureBase):
    pass


class TemperatureList(TemperatureBase):
    pass


class TemperatureFilterByCity(BaseModel):
    city_id: int | None = None


TemperatureFilterDependency = Annotated[
    TemperatureFilterByCity, Depends(TemperatureFilterByCity)
]
