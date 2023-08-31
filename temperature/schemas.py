from pydantic import BaseModel


class TemperatureBase(BaseModel):
    city_id: str
    date_time: str
    temperature: float


class Temperature(TemperatureBase):
    id: int

    class Config:
        from_attributes = True
