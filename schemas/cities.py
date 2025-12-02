from pydantic import BaseModel

class BaseCity(BaseModel):
    name: str
    additional_info: str

class CreateCity(BaseCity):
    pass

class GetCity(BaseCity):
    id: int

    class Config:
        from_attributes = True


class StatusMessage(BaseModel):
    message: str


class CityUpdate(BaseCity):
    name: str | None = None
    additional_info: str | None = None