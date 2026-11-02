from pydantic import BaseModel, ConfigDict


class CreateCitySchema(BaseModel):
    name: str
    additional_info: str

class ReadCitySchema(BaseModel):
    model_config = ConfigDict(from_attributes=True)

    id: int
    name: str
    additional_info: str