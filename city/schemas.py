import datetime
from pydantic import BaseModel


class City(BaseModel):
    id: int
    name: str
    additional_info: str

    class Config:
        orm_mode = True


class CitySchemaDetail(City):
    id: int

class Temperature(BaseModel):
    id: int
    city_id: int
    date_time: datetime
    temperature: float

    class Config:
        orm_mode = True