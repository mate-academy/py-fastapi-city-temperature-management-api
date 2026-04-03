from typing import List
from pydantic import BaseModel, ConfigDict
from src.base_schemas import TemperatureBase

class CityCreateOrUpdate(BaseModel):
    name: str
    additional_info: str


class CityRead(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    additional_info: str
    temperatures: List[TemperatureBase] = []
