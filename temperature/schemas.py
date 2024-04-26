from datetime import datetime
from pydantic import BaseModel
from sqlalchemy.orm import Relationship

from city.schemas import City


class TempBase(BaseModel):
    date_time: datetime
    temperature: float


class TempCreate(TempBase):
    pass


class Temp(TempBase):
    id: int
    city_id: int

    class Config:
        from_attributes = True
