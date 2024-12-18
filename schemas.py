from pydantic import BaseModel


# City schema
class CityBase(BaseModel):
    name: str
    country: str


class CityCreate(CityBase):
    pass


class CityOut(CityBase):
    id: int

    class Config:
        orm_mode = True


# Temperature schema
class TemperatureBase(BaseModel):
    city_id: int
    temperature: float
    time: str


class TemperatureCreate(TemperatureBase):
    pass


class TemperatureOut(TemperatureBase):
    id: int

    class Config:
        orm_mode = True
