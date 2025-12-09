from datetime import datetime

from pydantic import BaseModel


class TemperatureSchema(BaseModel):
    date_time: datetime
    temperature: float

    model_config = {
        "from_attributes": True
    }


class TemperatureDetailSchema(TemperatureSchema):
    id: int
    city_id: int
