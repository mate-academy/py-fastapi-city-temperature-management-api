from pydantic import BaseModel, Field

from src.weatherapi.schemas.temperature import TemperatureBase


class CityBase(BaseModel):
    name: str = Field(..., frozen=True, max_length=128)
    additional_info: str | None = None


class CityCreate(CityBase):
    pass


class CityRead(CityBase):
    id: int

    class Config:
        from_attributes = True


class CityReadWithTemperatures(CityRead):
    temperatures: list[TemperatureBase] | None = None

    class Config:
        from_attributes = True
