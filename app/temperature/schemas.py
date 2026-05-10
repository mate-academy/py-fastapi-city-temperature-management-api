from datetime import datetime

from pydantic import BaseModel


class TemperatureBase(BaseModel):
	date_time: datetime
	temperature: str


class TemperatureList(TemperatureBase):
	city_id: int
