from pydantic import BaseModel, Field, field_validator


class CityBase(BaseModel):
    name: str = Field(..., min_length=1, max_length=50)



class CityCreate(CityBase):
    additional_info: str | None = Field(None, min_length=1, max_length=500)

    @field_validator("name", mode="after")
    @classmethod
    def parse_name(cls, v):
        v.lower()
        v_list = v.split(" ")
        v_list = [word.capitalize() for word in v_list]
        return " ".join(v_list)

class CityRead(CityBase):
    id: int
    additional_info: str | None

    model_config = {
        "from_attributes": True
    }

class CityUpdate(CityCreate):
    pass
