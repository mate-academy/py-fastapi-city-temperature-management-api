from pydantic import BaseModel, ConfigDict


class CityDto(BaseModel):
    id: int
    name: str
    additional_info: str | None = None
    
    model_config = ConfigDict(from_attributes=True)


class CityCreateUpdateDto(BaseModel):
    name: str
    additional_info: str | None = None
    
    model_config = ConfigDict(from_attributes=True)
