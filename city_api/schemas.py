from pydantic import BaseModel


class CityBaseSchema(BaseModel):
    name: str
    additional_info: str


class CityCreateSchema(CityBaseSchema):
    pass


class CityResponseCreateSchema(CityCreateSchema):
    id: int


class CityMessageResponse(BaseModel):
    message: str
