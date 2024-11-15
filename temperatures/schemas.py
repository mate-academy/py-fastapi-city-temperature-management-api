from datetime import datetime

import pydantic


class TemperatureBase(pydantic.BaseModel):
    city_id: int
    date_time: datetime
    temperature: float


class Temperature(TemperatureBase):
    id: int

    class Config:
        from_attributes = True
