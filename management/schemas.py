from pydantic import BaseModel


class CityBase(BaseModel):
    name: str
    additional_info: str


class City(CityBase):
    id: int

    class Config:
        from_attributes = True


class CityCreate(CityBase):
    pass


class CityUpdate(CityBase):
    pass


class TemperatureBase(BaseModel):
    city_id: int
    date_time: str
    temperature: int
