from pydantic import BaseModel, ConfigDict, Field

from app.schemas import temperature_schema


class CityBase(BaseModel):
    name: str
    additional_info: str


class CityCreate(CityBase):
    pass


class City(CityBase):
    model_config = ConfigDict(from_attributes=True)

    id: int
    temperatures: list[temperature_schema.Temperature] = Field(
        default_factory=list
    )
