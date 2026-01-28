from typing import List

from pydantic import BaseModel, ConfigDict
from schemas.temperature import Temperature


class CityBase(BaseModel):
    name: str
    additional_info: str

class CityCreate(CityBase):
    pass

class City(CityBase):
    id: int

    model_config = ConfigDict(from_attributes=True)

class CityFull(City):
    temperatures: List[Temperature] = []
