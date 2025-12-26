from datetime import datetime
from typing import List

from pydantic import BaseModel


class TempSchema(BaseModel):
    id: int
    city_id: int
    date_time: datetime
    temperature: float | None

    model_config = {"from_attributes": True}


class TempListSchema(BaseModel):
    temps: List[TempSchema]
