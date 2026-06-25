from pydantic import BaseModel, ConfigDict


class CityBaseSchema(BaseModel):
    name: str
    additional_info: str | None = None


class CityCreateSchema(CityBaseSchema):
    pass


class CityUpdateSchema(CityBaseSchema):
    name: str | None = None


class CitySchema(CityBaseSchema):
    id: int

    model_config = ConfigDict(from_attributes=True)
