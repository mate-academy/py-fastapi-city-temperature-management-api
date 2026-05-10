from pydantic import BaseModel, ConfigDict
from app.schemas.temperature import TemperatureResponse


class CityBase(BaseModel):
    name: str
    additional_info: str | None = None


class CityCreate(CityBase):
    pass


class CityResponse(CityBase):
    id: int

    model_config = ConfigDict(from_attributes=True)


class CityWithTemperatures(CityResponse):
    temperatures: list[TemperatureResponse] = []
