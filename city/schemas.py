from pydantic import BaseModel, ConfigDict
from temperature.schemas import TemperatureResponse


class CityBase(BaseModel):
    name: str
    additional_info: str


class CityCreate(CityBase):
    pass


class CityResponse(CityBase):
    id: int
    temperatures: list[TemperatureResponse]

    model_config = ConfigDict(from_attributes=True)


class CityUpdate(CityBase):
    pass
