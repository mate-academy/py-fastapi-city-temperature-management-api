from pydantic import BaseModel


class CityCreateSchema(BaseModel):
    name: str
    additional_info: str

    class Config:
        from_attributes = True


class CityReadSchema(CityCreateSchema):
    id: int
