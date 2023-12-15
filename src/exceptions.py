from typing import Literal

from pydantic import BaseModel


class FetchTemperatureError(BaseModel):
    city_id: int | None
    city_name: str | None
    code: int | None
    message: str
    status: Literal["error"] = "error"
