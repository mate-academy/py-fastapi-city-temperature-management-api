from pydantic import BaseModel, ConfigDict

from src.schemas.temperature import TemperatureBaseSchema


class CityBaseSchema(BaseModel):
    name: str
    additional_info: str | None = None

    model_config = ConfigDict(from_attributes=True)


class CityRequestSchema(CityBaseSchema):
    pass


class CityResponseSchema(CityBaseSchema):
    id: int


class CityTemperatureResponseSchema(CityBaseSchema):
    id: int
    temperature: TemperatureBaseSchema | None = None
