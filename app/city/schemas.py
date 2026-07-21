from pydantic import BaseModel


class CityBaseModel(BaseModel):
    name: str
    additional_info: str
