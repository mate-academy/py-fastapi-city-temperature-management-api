from pydantic import (
    BaseModel,
    ConfigDict,
    Field
)


class CityReadSchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str = Field(min_length=1, max_length=55)
    additional_info: str


class CityCreateSchema(BaseModel):
    name: str
    additional_info: str
