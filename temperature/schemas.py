from pydantic import BaseModel


class TemperatureBaseSchema(BaseModel):
    city_id: int
    city_name: str
    max_temperature: float
