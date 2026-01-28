from pydantic import BaseModel, Field

class CityBase(BaseModel):
    name: str = Field(min_length=1, max_length=200)
    additional_info: str | None = None

class CityCreate(CityBase):
    pass

class CityUpdate(BaseModel):
    name: str | None = Field(default=None, min_length=1, max_length=200)
    additional_info: str | None = None

class CityRead(CityBase):
    id: int

    class Config:
        from_attributes = True
