from pydantic import BaseModel


# Optional class for return messages
class Message(BaseModel):
    message: str


class CityBase(BaseModel):
    name: str
    additional_info: str | None = None


class CityCreate(CityBase):
    pass


class CityUpdate(CityBase):
    pass


class City(CityBase):
    id: int

    class Config:
        from_attributes = True
