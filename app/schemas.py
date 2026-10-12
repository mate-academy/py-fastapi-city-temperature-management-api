from pydantic import BaseModel, ConfigDict
from datetime import datetime

class CityBase(BaseModel):
    name: str
    additional_info: str

class CityCreate(CityBase):
    pass

class CityResponse(CityBase):
    id: int

    model_config = ConfigDict(
        from_attributes=True
    )

class TemperatureResponse(BaseModel):
    id: int
    city_id: int
    date_time: datetime
    temperature: float

    model_config = ConfigDict(from_attributes=True)