from pydantic import BaseModel, ConfigDict, Field


class CityRequestSchema(BaseModel):
    name: str = Field(..., max_length=255)
    additional_info: str | None = Field(None, max_length=255)


class CityCreateSchema(CityRequestSchema):
    pass


class CityUpdateSchema(CityRequestSchema):
    pass


class CityResponseSchema(CityRequestSchema):
    id: int

    model_config = ConfigDict(from_attributes=True)


class PaginatedCityResponseSchema(BaseModel):
    cities: list[CityResponseSchema]
    total_items: int
    total_pages: int
    prev_page: str | None = None
    next_page: str | None = None

    model_config = ConfigDict(from_attributes=True)
