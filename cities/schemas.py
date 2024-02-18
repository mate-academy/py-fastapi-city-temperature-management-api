from pydantic import BaseModel, Field


class CityBase(BaseModel):
    name: str = Field(min_length=1, max_length=55)
    additional_info: str = Field(min_length=1, max_length=255)


class City(BaseModel):
    id: int
    name: str = Field(min_length=1, max_length=55)
    additional_info: str = Field(min_length=1, max_length=255)
