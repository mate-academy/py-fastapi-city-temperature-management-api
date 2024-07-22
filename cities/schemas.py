from pydantic import BaseModel

class CityBaseSchema(BaseModel):
    name: str
    additional_info: str

class CityCreateSchema(CityBaseSchema):
    pass

class CitySchema(CityBaseSchema):
    id: int
    name: str
    additional_info: str

    class Config:
        orm_mode = True