from datetime import datetime

from pydantic import BaseModel, ConfigDict, Field


class CityBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=100, examples=["Kyiv"])
    additional_info: str | None = Field(
        default=None, max_length=500, examples=["Capital of Ukraine"]
    )


class CityCreate(CityBase):
    pass


class CityUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=100)
    additional_info: str | None = Field(default=None, max_length=500)


class CityResponse(CityBase):
    model_config = ConfigDict(from_attributes=True)

    id: int


class TemperatureResponse(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    city_id: int
    date_time: datetime
    temperature: float


class TemperatureUpdateResult(BaseModel):
    updated: int
    failed: list[str] = Field(default_factory=list)
    message: str
