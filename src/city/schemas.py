from typing import Optional

from pydantic import BaseModel


class BaseCity(BaseModel):
    name: str
    additional_info: Optional[str]


class CreateCity(BaseCity):
    ...


class City(BaseCity):
    id: int
