from __future__ import annotations

from typing import Optional, TYPE_CHECKING

from pydantic import BaseModel, ConfigDict

if TYPE_CHECKING:
    from temperature.schemas import TemperatureRead


class CityBase(BaseModel):
    name: str
    additional_info: Optional[str] = None


class CityRead(CityBase):
    id: int
    temperatures: list["TemperatureRead"] = []

    model_config = ConfigDict(from_attributes=True)


class CityCreate(CityBase):
    additional_info: Optional[str] = None


class CityUpdate(CityBase):
    name: Optional[str] = None
    additional_info: Optional[str] = None


# Rebuild the model after imports to resolve forward references
def _rebuild_models():
    from temperature.schemas import TemperatureRead
    CityRead.model_rebuild()


# Call this when the module is imported
try:
    _rebuild_models()
except ImportError:
    # Temperature schemas might not be available yet
    pass
