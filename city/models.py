from pydantic import BaseModel


class CityModel(BaseModel):
    id: int
    name: str
    additional_info: str
