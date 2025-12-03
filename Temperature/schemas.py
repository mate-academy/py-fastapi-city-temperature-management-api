from datetime import date

from pydantic import BaseModel


class TemperatureBase(BaseModel):
    city_id: int
    date_time: date
    temperature: float

    model_config = {
        "from_attributes": True
    }


class Temperature(TemperatureBase):
    id: int

    model_config = {
        "from_attributes": True
    }


class TemperatureCreate(TemperatureBase):
    pass


class TemperatureUpdate(TemperatureBase):
    pass
