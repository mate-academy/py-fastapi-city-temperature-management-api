from pydantic import BaseModel, ConfigDict


class City(BaseModel):
    id: int
    name: str
    additional_info: str

    model_config = ConfigDict(from_attributes=True)
