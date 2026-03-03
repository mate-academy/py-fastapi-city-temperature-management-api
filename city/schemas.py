from pydantic import BaseModel


class CityBaseSchemas(BaseModel):
    id: int
    name: str
    additional_info: str


class CreateCitySchemas(BaseModel):
    name: str
    additional_info: str


class UpdateCitySchemas(BaseModel):
    name: str | None = None
    additional_info: str | None = None


class MessageSchema(BaseModel):
    message: str
