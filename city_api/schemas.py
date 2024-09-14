from pydantic import BaseModel


class CityBase(BaseModel):
    name: str
    additional_info: str


class CityCreate(CityBase):
    pass


class CityList(CityBase):
    id: int

    model_config = {
        "from_attributes": True
    }
