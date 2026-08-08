from pydantic import BaseModel, ConfigDict


class CityCreate(BaseModel):
    name: str
    additional_info: str | None = None


class CityResponse(CityCreate):
    model_config = ConfigDict(from_attributes=True)

    id: int