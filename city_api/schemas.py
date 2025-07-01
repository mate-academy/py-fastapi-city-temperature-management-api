from datetime import datetime

from pydantic import BaseModel


class CityCreateResponseSchema(BaseModel):
    id: int
    name: str
    additional_info: str


class CityCreateRequest(BaseModel):
    name: str
    additional_info: str


class UpdateTemperatureSchemaRequest(BaseModel):
    last_updated: datetime
    temp_c: float
    wind_kmh: float

    class Config:
        json_encoders = {
            datetime: lambda x: x.strftime("%Y-%m-%d %H:%M")
        }



class TemperatureResponse(BaseModel):
    id: int
    city_id: int
    temperature: float
    date_time: datetime | None
