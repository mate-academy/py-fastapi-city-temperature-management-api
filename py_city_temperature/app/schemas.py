from datetime import datetime
from pydantic import BaseModel


# --- City ---
class CityCreate(BaseModel):
    name: str
    additional_info: str | None = None


class CityUpdate(BaseModel):
    name: str | None = None
    additional_info: str | None = None


class CityRead(BaseModel):
    id: int
    name: str
    additional_info: str | None

    model_config = {"from_attributes": True}


# --- Temperature ---
class TemperatureRead(BaseModel):
    id: int
    city_id: int
    date_time: datetime
    temperature: float

    model_config = {"from_attributes": True}
