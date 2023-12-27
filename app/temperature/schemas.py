from pydantic import BaseModel


class TemperatureBase(BaseModel):
    city_id: int
    date_time: str
    temperature: int
