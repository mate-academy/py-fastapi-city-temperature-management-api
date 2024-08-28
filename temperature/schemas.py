from pydantic import BaseModel


class TemperatureBase(BaseModel):
    city_id: int
    temperature: float
