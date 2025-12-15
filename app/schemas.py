from datetime import datetime
from pydantic import BaseModel, ConfigDict


# -------- Cities --------
class CityBase(BaseModel):
    name: str
    additional_info: str | None = None


class CityCreate(CityBase):
    pass


class CityRead(CityBase):
    id: int
    model_config = ConfigDict(from_attributes=True)


# -------- Temperatures --------
class TemperatureRead(BaseModel):
    id: int
    city_id: int
    date_time: datetime
    temperature: float

    model_config = ConfigDict(from_attributes=True)
