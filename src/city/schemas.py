from pydantic import BaseModel, Field, field_validator


class CityBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)



class CityCreate(CityBase):
    additional_info: str | None = Field(None, min_length=1, max_length=500)

    @field_validator("name", mode="after")
    @classmethod
    def parse_name(cls, v):
        return v.strip().lower().capitalize()

class CityRead(CityBase):
    id: int
    additional_info: str

    model_config = {
        "from_attributes": True
    }

class CityUpdate(CityCreate):
    pass
