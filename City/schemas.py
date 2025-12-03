from pydantic import BaseModel


class CityBase(BaseModel):
    name: str
    additional_info: str

    model_config = {
        "from_attributes": True
    }


class City(CityBase):
    id: int

    model_config ={
        "from_attributes": True
    }


class CityCreate(CityBase):
    pass

class CityUpdate(CityBase):
    pass
