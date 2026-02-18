from pydantic import BaseModel, ConfigDict


class CityCreateUpdateSchema(BaseModel):
    name: str
    additional_info: str


class CityReadSchema(CityCreateUpdateSchema):
    id: int

    model_config = ConfigDict(from_attributes=True)
