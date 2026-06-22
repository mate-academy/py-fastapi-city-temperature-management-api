from pydantic import BaseModel, Field, ConfigDict
from app.schemas.temperature import Temperature


class CityBase(BaseModel):
    name: str
    additional_info: str | None = None


class CityCreate(CityBase):
    pass


class City(CityBase):
    id: int
    temperatures: list[Temperature] = Field(default_factory=list)

    model_config = ConfigDict(from_attributes=True)
