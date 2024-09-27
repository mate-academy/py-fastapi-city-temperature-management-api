from pydantic import BaseModel, PastDatetime


class TemperatureBase(BaseModel):
    city_id: int
    date_time: PastDatetime
    temperature: float


class TemperatureCreate(TemperatureBase):
    pass


class Temperature(TemperatureBase):
    id: int

    class Config:
        from_attributes = True
