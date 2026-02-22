from datetime import datetime


from pydantic import BaseModel
from ..cities.schemas import CityOut


class TemperatureBase(BaseModel):
    city_id: int
    date_time: datetime
    temperature: float


class TemperatureOutCity(TemperatureBase):
    id: int

    city: CityOut

    model_config = {"from_attributes": True}

class TemperatureOut(TemperatureBase):
    id: int

    model_config = {"from_attributes": True}

