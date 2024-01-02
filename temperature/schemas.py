from pydantic import BaseModel


class BaseTemperature(BaseModel):
    city_id: int
    date_time: str
    temperature: float


class TemperatureCreate(BaseTemperature):
    pass


class Temperature(BaseTemperature):
    id: int

    class Config:
        from_attributes = True
