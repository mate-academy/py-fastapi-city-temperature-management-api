from pydantic import BaseModel, ConfigDict, Field


class CityAdditionalInfo(BaseModel):
    latitude: float = Field(ge=-90, le=90)
    longitude: float = Field(ge=-180, le=180)


class CityBase(BaseModel):
    name: str
    additional_info: CityAdditionalInfo


class CityCreate(CityBase):
    pass


class CityRead(CityBase):
    id: int

    model_config = ConfigDict(from_attributes=True)
