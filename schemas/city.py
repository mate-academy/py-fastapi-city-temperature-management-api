from models.city import City
from pydantic import BaseModel, constr


class CityCreateSchema(BaseModel):
    name: constr(min_length=1, max_length=100)
    additional_info: constr(max_length=255) | None = None


class CityReadSchema(BaseModel):
    id: int
    name: str
    additional_info: str | None = None

    class Config:
        from_attributes = True
