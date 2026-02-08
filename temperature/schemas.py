import datetime

from pydantic import BaseModel


class Temperature(BaseModel):
    id: int
    city_id: int
    date_time: datetime.datetime
    temperature: float

    class Config:
        from_attributes = True
        orm_mode = True
