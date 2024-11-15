from typing import Optional

import pydantic


class CityBase(pydantic.BaseModel):
    name: str
    additional_info: Optional[str] = None


class CityCreate(CityBase):
    pass


class City(CityBase):
    id: int

    class Config:
        orm_mode = True


class CityUpdate(pydantic.BaseModel):
    name: Optional[str] = None
    additional_info: Optional[str] = None


class Message(pydantic.BaseModel):
    message: str
