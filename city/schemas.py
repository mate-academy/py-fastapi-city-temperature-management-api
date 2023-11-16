from typing import Optional

from pydantic import BaseModel


class CityBaseSerializer(BaseModel):
    name: str
    additional_info: Optional[str] = None


class CityCreateSerializer(CityBaseSerializer):
    pass


class CitySerializer(CityBaseSerializer):
    id: int

    class Config:
        orm_mode = True
