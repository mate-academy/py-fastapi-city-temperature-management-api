from pydantic import BaseModel
from typing import Optional, List
from datetime import datetime

# --- City Schemas ---
class CityBase(BaseModel):
    name: str
    additional_info: Optional[str] = None

class CityCreate(CityBase):
    pass

class CityResponse(CityBase):
    id: int
    
    class Config:
        from_attributes = True

# --- Temperature Schemas ---
class TemperatureBase(BaseModel):
    temperature: float

class TemperatureResponse(TemperatureBase):
    id: int
    city_id: int
    date_time: datetime

    class Config:
        from_attributes = True
